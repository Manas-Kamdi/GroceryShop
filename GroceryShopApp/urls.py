from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("products/", views.products, name="products"),
    path("add-product/", views.add_product, name="add_product"),
    path("about/", views.about, name="about"),
    path("cart/", views.cart, name="cart"),
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("update-cart-item/", views.update_cart_item, name="update_cart_item"),
    path("remove-from-cart/", views.remove_from_cart, name="remove_from_cart"),
    path("profile/", views.profile, name="profile"),
    path("payment/", views.payment, name="payment"),
    path("create-razorpay-order/", views.create_razorpay_order, name="create_razorpay_order"),
    path("process-payment/", views.process_payment, name="process_payment"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("track-order/<str:order_number>/", views.track_order, name="track_order"),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('staff/confirm_order/<int:order_id>/', views.admin_confirm_order, name='admin_confirm_order'),
    path('staff/orders/', views.admin_orders, name='admin_orders'),
    path('staff/orders/confirm/<int:order_id>/', views.admin_confirm_order, name='admin_confirm_order'),
    path('order-success/', views.order_success, name='order_success'),
    
    # 🚚 Delivery Boy Routes
    path("delivery/dashboard/", views.delivery_dashboard, name="delivery_dashboard"),
    path("delivery/toggle-status/", views.toggle_delivery_status, name="toggle_delivery_status"),
    path("delivery/accept-order/<int:order_id>/", views.delivery_accept_order, name="delivery_accept_order"),
    path("delivery/update-status/<int:order_id>/<str:status>/", views.delivery_update_status, name="delivery_update_status"),
]