from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.conf import settings
import uuid
import hashlib
import hmac
import json
from .models import UserProfile, Product, Cart, CartItem, Order, OrderItem


# Home Page
def home(request):
    context = {}
    if request.user.is_authenticated:
        context['welcome_message'] = f"Welcome back, {request.user.first_name or request.user.username}!"
    return render(request, "Home.html", context)


# Login Page
def login(request):
    if request.method == "POST":
        identifier = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        # Try direct username (could be email or username)
        user = authenticate(request, username=identifier, password=password)
        if user is None:
            # If identifier looks like an email, resolve to username
            lookup_email = identifier.lower()
            try:
                account = User.objects.get(email__iexact=lookup_email)
                user = authenticate(request, username=account.username, password=password)
            except User.DoesNotExist:
                user = None
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("home")
        messages.error(request, "Invalid email or password.")
    return render(request, "login.html")


# Signup Page
def signup(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone = request.POST.get("number", "").strip()
        address = request.POST.get("address", "").strip()
        password = request.POST.get("password", "")
        confirm = request.POST.get("c-password", "")

        errors = []
        if not email:
            errors.append("Email is required.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            errors.append("Email already registered.")

        if errors:
            return render(request, "signup.html", {"errors": errors})

        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        UserProfile.objects.create(user=user, phone=phone, address=address)
        messages.success(request, "Registration successful. Please log in.")
        return redirect("login")

    return render(request, "signup.html")


# Logout
def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


# Dashboard Page
@login_required
def dashboard(request):
    return render(request, "Home.html")

# Products Page
def products(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Product.objects.values_list('category', flat=True).distinct().exclude(category__isnull=True).exclude(category='')
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, "Product.html", context)

# About Page
def about(request):
    return render(request, "About.html")

# Add Product Page (Admin only)
@login_required
def add_product(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to add products.")
        return redirect("home")
    
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price", "").strip()
        category = request.POST.get("category", "").strip()
        stock_quantity = request.POST.get("stock_quantity", "0").strip()
        
        errors = []
        if not name:
            errors.append("Product name is required.")
        if not price:
            errors.append("Price is required.")
        elif not price.replace('.', '').isdigit():
            errors.append("Price must be a valid number.")
        if not category:
            errors.append("Category is required.")
        
        if errors:
            return render(request, "add_product.html", {"errors": errors})
        
        try:
            product = Product.objects.create(
                name=name,
                description=description,
                price=float(price),
                category=category,
                stock_quantity=int(stock_quantity) if stock_quantity else 0
            )
            
            # Handle image upload
            if 'image' in request.FILES:
                product.image = request.FILES['image']
                product.save()
            
            messages.success(request, f"Product '{product.name}' added successfully!")
            return redirect("products")
            
        except Exception as e:
            messages.error(request, f"Error adding product: {str(e)}")
    
    return render(request, "add_product.html")


# Cart Page
@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.total_price,
        'total_items': cart.total_items,
    }
    return render(request, "Cart.html", context)

# Add to Cart
@login_required
@require_POST
def add_to_cart(request):
    print(f"Add to cart request from user: {request.user}")
    print(f"POST data: {request.POST}")
    
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    if not product_id:
        return JsonResponse({
            'success': False,
            'message': 'Product ID is required'
        })
    
    try:
        product = get_object_or_404(Product, id=product_id)
        print(f"Product found: {product.name}")
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        print(f"Cart {'created' if created else 'found'}: {cart}")
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            print(f"Updated existing cart item quantity to: {cart_item.quantity}")
        else:
            print(f"Created new cart item with quantity: {cart_item.quantity}")
        
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart',
            'cart_total': cart.total_items
        })
    except Exception as e:
        print(f"Error in add_to_cart: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'Error adding item to cart: {str(e)}'
        })

# Update Cart Item
@login_required
@require_POST
def update_cart_item(request):
    cart_item_id = request.POST.get('cart_item_id')
    quantity = int(request.POST.get('quantity', 1))
    
    try:
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        
        if quantity <= 0:
            cart_item.delete()
            message = 'Item removed from cart'
        else:
            cart_item.quantity = quantity
            cart_item.save()
            message = 'Cart updated'
        
        cart = cart_item.cart
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_total': cart.total_items,
            'item_total': cart_item.total_price,
            'cart_total_price': cart.total_price
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error updating cart'
        })

# Remove from Cart
@login_required
@require_POST
def remove_from_cart(request):
    cart_item_id = request.POST.get('cart_item_id')
    
    try:
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        product_name = cart_item.product.name
        cart_item.delete()
        
        cart = Cart.objects.get(user=request.user)
        return JsonResponse({
            'success': True,
            'message': f'{product_name} removed from cart',
            'cart_total': cart.total_items,
            'cart_total_price': cart.total_price
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error removing item from cart'
        })


# Profile Page
@login_required
def profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", "").strip()
        user.last_name = request.POST.get("last_name", "").strip()
        user.save()
        
        profile_obj, created = UserProfile.objects.get_or_create(user=user)
        profile_obj.phone = request.POST.get("phone", "").strip()
        profile_obj.address = request.POST.get("address", "").strip()
        profile_obj.area = request.POST.get("area", "").strip()
        profile_obj.landmark = request.POST.get("landmark", "").strip()
        profile_obj.pincode = request.POST.get("pincode", "").strip()
        
        # Handle profile photo upload
        if 'profile_photo' in request.FILES:
            print(f"Profile photo received: {request.FILES['profile_photo'].name}")
            profile_obj.profile_photo = request.FILES['profile_photo']
        else:
            print("No profile photo in request.FILES")
        
        # Handle profile photo removal
        if request.POST.get('remove_photo') == 'true':
            if profile_obj.profile_photo:
                profile_obj.profile_photo.delete(save=False)
                profile_obj.profile_photo = None
        
        profile_obj.save()
        
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")
    
    # Ensure user has a cart so template can safely access user.cart
    Cart.objects.get_or_create(user=request.user)
    return render(request, "profile.html")

# Payment Page
@login_required
def payment(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty. Add some items before checkout.")
        return redirect("cart")
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.total_price,
        'total_items': cart.total_items,
    }
    return render(request, "Payment.html", context)

# Create Razorpay Order
@login_required
@require_POST
def create_razorpay_order(request):
    try:
        amount = int(request.POST.get('amount', 0))
        if amount <= 0:
            return JsonResponse({
                'success': False,
                'message': 'Invalid amount'
            })
        
        # Generate order ID (you should use Razorpay API here)
        # For demo purposes, we'll create a simple order ID
        order_id = f"order_{uuid.uuid4().hex[:10]}"
        
        # In a real implementation, you would call Razorpay API here
        # For now, we'll return a mock order ID
        return JsonResponse({
            'success': True,
            'order_id': order_id,
            'amount': amount
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error creating order: {str(e)}'
        })

# Process Payment
@login_required
@require_POST
def process_payment(request):
    try:
        # Get cart and items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        
        if not cart_items.exists():
            return JsonResponse({
                'success': False,
                'message': 'Cart is empty'
            })
        
        # Get form data
        delivery_name = request.POST.get('delivery_name', '').strip()
        delivery_phone = request.POST.get('delivery_phone', '').strip()
        delivery_address = request.POST.get('delivery_address', '').strip()
        delivery_area = request.POST.get('delivery_area', '').strip()
        delivery_landmark = request.POST.get('delivery_landmark', '').strip()
        delivery_pincode = request.POST.get('delivery_pincode', '').strip()
        payment_method = request.POST.get('payment_method', '')
        
        # Validate required fields
        if not all([delivery_name, delivery_phone, delivery_address, delivery_area, delivery_pincode]):
            return JsonResponse({
                'success': False,
                'message': 'Please fill all required delivery address fields'
            })
        
        # Generate order number
        order_number = f"ORD{timezone.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            total_amount=cart.total_price,
            payment_status='paid' if payment_method == 'razorpay' else 'pending',
            payment_id=request.POST.get('razorpay_payment_id', ''),
            delivery_name=delivery_name,
            delivery_phone=delivery_phone,
            delivery_address=delivery_address,
            delivery_area=delivery_area,
            delivery_landmark=delivery_landmark,
            delivery_pincode=delivery_pincode,
            order_status='confirmed' if payment_method == 'razorpay' else 'pending'
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
        
        return JsonResponse({
            'success': True,
            'order_number': order_number,
            'message': 'Order placed successfully!'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error processing payment: {str(e)}'
        })

# My Orders
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, "my_orders.html", context)


# Order Tracking Page
@login_required
def track_order(request, order_number: str):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    # Define the canonical progression of statuses
    steps = [
        { 'key': 'pending',    'label': 'Pending',    'desc': 'Order received, awaiting confirmation.' },
        { 'key': 'confirmed',  'label': 'Confirmed',  'desc': 'Order confirmed and being prepared.' },
        { 'key': 'processing', 'label': 'Processing', 'desc': 'Items are being packed for shipment.' },
        { 'key': 'shipped',    'label': 'Shipped',    'desc': 'Order shipped and on the way.' },
        { 'key': 'delivered',  'label': 'Delivered',  'desc': 'Order delivered successfully.' },
    ]

    # Compute current index
    step_index_by_key = {s['key']: idx for idx, s in enumerate(steps)}
    current_index = step_index_by_key.get(order.order_status, 0)

    context = {
        'order': order,
        'steps': steps,
        'current_index': current_index,
    }
    return render(request, "order_tracking.html", context)