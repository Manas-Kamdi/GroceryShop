from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Product, Cart, CartItem, Order, OrderItem, UserProfile
import uuid
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


# 🏠 Home Page
def home(request):
    products = Product.objects.all()[:8]
    return render(request, "Home.html", {"products": products})

# 🔑 Login Page
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Find user by email or username
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            username = email

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email/username or password")
    return render(request, "Login.html")

# 🧾 Signup Page
def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['number']
        address = request.POST['address']
        password = request.POST['password']
        confirm_password = request.POST['c-password']

        # check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists! Please use a different one.")
            return redirect('signup')

        # check password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # create user
        user = User.objects.create_user(username=name, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'Signup.html')

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
        Product.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description", ""),
            price=request.POST.get("price"),
            category=request.POST.get("category", ""),
            stock_quantity=request.POST.get("stock_quantity", 0),
            image=request.FILES.get("image")
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
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.total_price for item in cart_items)
    return render(request, "Cart.html", {"cart_items": cart_items, "total_items": total_items, "total_price": total_price})

# ➕ Add to Cart
@login_required
@require_POST
def add_to_cart(request):
    product_id = request.POST.get("product_id")
    try:
        product = Product.objects.get(id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return JsonResponse({"success": True})
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"})

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
        return JsonResponse({"success": True})
    except CartItem.DoesNotExist:
        return JsonResponse({"error": "Cart item not found"})

# ❌ Remove from Cart
@login_required
@require_POST
def remove_from_cart(request):
    item_id = request.POST.get("item_id")
    try:
        CartItem.objects.get(id=item_id, cart__user=request.user).delete()
        return JsonResponse({"success": True})
    except CartItem.DoesNotExist:
        return JsonResponse({"error": "Cart item not found"})

# 👤 Profile Page
@login_required
def profile(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', user.email)
        user.save()

        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.area = request.POST.get('area', '')
        profile.landmark = request.POST.get('landmark', '')
        profile.pincode = request.POST.get('pincode', '')

        if 'profile_photo' in request.FILES:
            profile.profile_photo = request.FILES['profile_photo']

        if 'remove_photo' in request.POST and profile.profile_photo:
            profile.profile_photo.delete(save=False)
            profile.profile_photo = None

        profile.save()
        messages.success(request, "✅ Profile updated successfully!")
        return redirect('profile')

    return render(request, 'profile.html', {'user': user, 'profile': profile})

# 💳 Payment Page
@login_required
def payment(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("cart")
    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.total_price for item in cart_items)
    return render(request, "Payment.html", {"cart_items": cart_items, "total_price": total_price})

# 💰 Process Payment
@login_required
@require_POST
def process_payment(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items.exists():
        return JsonResponse({"error": "Cart is empty"})

    order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    total_amount = sum(item.total_price for item in cart_items)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    order = Order.objects.create(
        user=request.user,
        order_number=order_number,
        total_amount=total_amount,
        delivery_name=request.POST.get("delivery_name", request.user.first_name),
        delivery_phone=request.POST.get("delivery_phone", profile.phone),
        delivery_address=request.POST.get("delivery_address", profile.address),
        delivery_area=request.POST.get("delivery_area", profile.area),
        delivery_landmark=request.POST.get("delivery_landmark", profile.landmark),
        delivery_pincode=request.POST.get("delivery_pincode", profile.pincode),
        payment_status="paid",
    )

    for cart_item in cart_items:
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity, price=cart_item.product.price)
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
    order_status_list = [
        ("pending", "📋", "Pending"),
        ("confirmed", "✅", "Confirmed"),
        ("processing", "🔄", "Processing"),
        ("shipped", "🚚", "Shipped"),
        ("delivered", "📦", "Delivered"),
    ]
    return render(request, "TrackOrder.html", {"order": order, "order_status_list": order_status_list})

# ❌ Cancel Order
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.order_status != 'cancelled':
        order.order_status = 'cancelled'
        order.save()
        messages.success(request, f"Order #{order.order_number} cancelled.")
    else:
        messages.info(request, "Order already cancelled.")
    return redirect('my_orders')

# ✅ Admin Views
@user_passes_test(lambda u: u.is_staff)
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin_orders.html', {'orders': orders})

@user_passes_test(lambda u: u.is_staff)
def admin_confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.order_status == 'pending':
        order.order_status = 'confirmed'
        order.save()
        messages.success(request, f"Order #{order.order_number} confirmed by Admin.")
    else:
        messages.warning(request, f"Order #{order.order_number} cannot be confirmed (already {order.order_status}).")
    return redirect('admin_orders')



@login_required
@require_POST
@csrf_exempt
def create_razorpay_order(request):
    if request.method == "POST":
        amount = int(request.POST.get("amount", 0))
        if amount <= 0:
            return JsonResponse({"success": False, "message": "Invalid amount"})

        try:
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )

            payment = client.order.create({
                "amount": amount,
                "currency": "INR",
                "payment_capture": "1"
            })

            return JsonResponse({
                "success": True,
                "order_id": payment["id"],
                "amount": amount,
                "currency": "INR"
            })
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request"})


def order_success(request):
    order_no = request.GET.get('order')
    return render(request, 'order_success.html', {'order_no': order_no})
