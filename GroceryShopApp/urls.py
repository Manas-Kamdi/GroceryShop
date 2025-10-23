from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add-product/", views.add_product, name="add_product"),
    path("edit-product/<int:product_id>/", views.edit_product, name="edit_product"),
    path("delete-product/<int:product_id>/", views.delete_product, name="delete_product"),
]
