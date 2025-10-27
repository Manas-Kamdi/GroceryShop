from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Product, Cart, CartItem, Order, OrderItem, UserProfile

# 🏠 Home Page
def home(request):
    products = Product.objects.all()[:8]  # Show only 8 products on home page
    return render(request, "Home.html", {"products": products})

# 🔑 Login Page
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Try to find user by email first, then by username
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            username = email  # Try as username if email not found
        
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email/username or password")
    return render(request, "Login.html")

# 🧾 Signup Page
def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        number = request.POST.get("number")
        address = request.POST.get("address")
        password = request.POST.get("password")
        c_password = request.POST.get("c-password")
        
        # Validation
        if password != c_password:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
        else:
            # Create user with email as username
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                phone=number,
                address=address
            )
            
            # Create cart for user
            Cart.objects.create(user=user)
            
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
    return render(request, "Signup.html")

# 🚪 Logout
def logout(request):
    auth_logout(request)
    return redirect("login")

# 🧭 Dashboard
@login_required
def dashboard(request):
    return render(request, "Dashboard.html")

# 🛒 Products Page
def products(request):
    products = Product.objects.all()
    categories = Product.objects.values_list('category', flat=True).distinct().exclude(category__isnull=True).exclude(category='')
    return render(request, "Products.html", {"products": products, "categories": categories})

# ➕ Add Product (Admin)
@login_required
def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        price = request.POST.get("price")
        category = request.POST.get("category", "")
        stock_quantity = request.POST.get("stock_quantity", 0)
        image = request.FILES.get("image")
        
        Product.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            stock_quantity=stock_quantity,
            image=image
        )
        messages.success(request, "Product added successfully!")
        return redirect("products")
    return render(request, "AddProduct.html")

# ℹ️ About Page
def about(request):
    return render(request, "About.html")

# 🛒 Cart Page
@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Calculate totals
    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.total_price for item in cart_items)
    
    return render(request, "Cart.html", {
        "cart_items": cart_items, 
        "cart": cart,
        "total_items": total_items,
        "total_price": total_price
    })

# ➕ Add to Cart
@login_required
@require_POST
def add_to_cart(request):
    product_id = request.POST.get("product_id")
    if not product_id:
        return JsonResponse({"error": "Product ID is required"})
    
    try:
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return JsonResponse({"success": True, "message": "Product added to cart"})
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"})
    except Exception as e:
        return JsonResponse({"error": str(e)})

# 🔄 Update Cart Item
@login_required
@require_POST
def update_cart_item(request):
    item_id = request.POST.get("item_id")
    quantity = int(request.POST.get("quantity", 1))
    
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({"success": True, "message": "Cart updated"})
    except CartItem.DoesNotExist:
        return JsonResponse({"error": "Cart item not found"})
    except Exception as e:
        return JsonResponse({"error": str(e)})

# ❌ Remove from Cart
@login_required
@require_POST
def remove_from_cart(request):
    item_id = request.POST.get("item_id")
    
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()
        return JsonResponse({"success": True, "message": "Item removed from cart"})
    except CartItem.DoesNotExist:
        return JsonResponse({"error": "Cart item not found"})
    except Exception as e:
        return JsonResponse({"error": str(e)})

# 👤 Profile Page
@login_required
def profile(request):
    if request.method == "POST":
        # Update user fields
        user = request.user
        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.email = request.POST.get("email", user.email)
        user.save()
        
        # Update or create profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.phone = request.POST.get("phone", "")
        profile.address = request.POST.get("address", "")
        profile.area = request.POST.get("area", "")
        profile.landmark = request.POST.get("landmark", "")
        profile.pincode = request.POST.get("pincode", "")
        
        # Handle profile photo
        if request.FILES.get("profile_photo"):
            try:
                # Delete old photo if exists
                if profile.profile_photo:
                    profile.profile_photo.delete()
                profile.profile_photo = request.FILES.get("profile_photo")
            except Exception as e:
                messages.error(request, f"Error uploading photo: {str(e)}")
        elif request.POST.get("remove_photo"):
            try:
                if profile.profile_photo:
                    profile.profile_photo.delete()
                profile.profile_photo = None
            except Exception as e:
                messages.error(request, f"Error removing photo: {str(e)}")
        
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")
    
    # Ensure user has a profile and cart
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    return render(request, "Profile.html", {"profile": profile})

# 💳 Payment Page
@login_required
def payment(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Add some products first!")
        return redirect("cart")
    
    # Calculate totals
    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.total_price for item in cart_items)
    
    return render(request, "Payment.html", {
        "cart_items": cart_items, 
        "cart": cart,
        "total_items": total_items,
        "total_price": total_price
    })

# 💰 Razorpay Order Creation
@login_required
@require_POST
def create_razorpay_order(request):
    # Mock Razorpay order creation - replace with actual API call
    import uuid
    order_id = str(uuid.uuid4())
    return JsonResponse({"order_id": order_id, "status": "created"})

# 🧾 Process Payment
@login_required
@require_POST
def process_payment(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if not cart_items.exists():
        return JsonResponse({"error": "Cart is empty"})
    
    # Create order
    import uuid
    order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    total_amount = sum(item.total_price for item in cart_items)
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    order = Order.objects.create(
        user=request.user,
        order_number=order_number,
        total_amount=total_amount,
        delivery_name=request.POST.get("delivery_name", request.user.first_name or ""),
        delivery_phone=request.POST.get("delivery_phone", profile.phone or ""),
        delivery_address=request.POST.get("delivery_address", profile.address or ""),
        delivery_area=request.POST.get("delivery_area", profile.area or ""),
        delivery_landmark=request.POST.get("delivery_landmark", profile.landmark or ""),
        delivery_pincode=request.POST.get("delivery_pincode", profile.pincode or ""),
        payment_status="paid"
    )
    
    # Create order items
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
    
    # Clear cart
    cart_items.delete()
    
    return JsonResponse({"success": True, "order_number": order_number})

# 📦 My Orders
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "my_orders.html", {"orders": orders})

# 🚚 Track Order
@login_required
def track_order(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    # Define the order statuses and icons here (Python handles .split)
    order_status_list = [
        ("pending", "📋", "Pending"),
        ("confirmed", "✅", "Confirmed"),
        ("processing", "🔄", "Processing"),
        ("shipped", "🚚", "Shipped"),
        ("delivered", "📦", "Delivered"),
    ]

    return render(request, "TrackOrder.html", {
        "order": order,
        "order_status_list": order_status_list
    })