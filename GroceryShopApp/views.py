from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required   # ✅ Added this import
from django.core.files.storage import FileSystemStorage
from .models import Product


# 🏠 Home Page
def home(request):
    products = Product.objects.all()
    return render(request, "Home.html", {"products": products})


# 👤 Dashboard (Protected Page)
@login_required(login_url="login")   # ✅ Added login_url to redirect if not logged in
def dashboard(request):
    return render(request, "dashboard.html")


# 📝 Signup Page
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validation checks
        errors = []
        if password != confirm_password:
            errors.append("Passwords do not match.")
        if User.objects.filter(username=username).exists():
            errors.append("Username already exists.")
        if User.objects.filter(email=email).exists():
            errors.append("Email already registered.")

        if errors:
            return render(request, "Signup.html", {"errors": errors})

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")

    return render(request, "Signup.html")


# 🔐 Login Page
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "Login.html")

    return render(request, "Login.html")


# 🚪 Logout
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


# ➕ Add Product (Optional: Protect with login)
@login_required(login_url="login")
def add_product(request):
    if request.method == "POST" and request.FILES.get("image"):
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES["image"]

        # Save image and product
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        Product.objects.create(
            name=name, price=price, description=description, image=uploaded_file_url
        )
        messages.success(request, "Product added successfully!")
        return redirect("home")

    return render(request, "AddProduct.html")


# ❌ Delete Product
@login_required(login_url="login")
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, "Product deleted successfully!")
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
    return redirect("home")


# ✏️ Edit Product
@login_required(login_url="login")
def edit_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect("home")

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.description = request.POST.get("description")

        if request.FILES.get("image"):
            fs = FileSystemStorage()
            filename = fs.save(request.FILES["image"].name, request.FILES["image"])
            product.image = fs.url(filename)

        product.save()
        messages.success(request, "Product updated successfully!")
        return redirect("home")

    return render(request, "EditProduct.html", {"product": product})
