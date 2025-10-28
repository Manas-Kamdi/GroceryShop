from django.contrib import admin
from .models import Product, UserProfile, Cart, CartItem, Order, OrderItem

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'stock_quantity', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description', 'category']
    list_editable = ['price', 'stock_quantity']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_quantity')
        }),
        ('Image', {
            'fields': ('image',)
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address']
    search_fields = ['user__username', 'user__email', 'phone', 'address']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'created_at']
    readonly_fields = ['total_items', 'total_price']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'total_price']
    list_filter = ['cart__user', 'product__category']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'order_status', 'payment_status', 'created_at']
    list_filter = ['order_status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'total_amount', 'order_status', 'payment_status', 'payment_id')
        }),
        ('Delivery Address', {
            'fields': ('delivery_name', 'delivery_phone', 'delivery_address', 'delivery_area', 'delivery_landmark', 'delivery_pincode')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # ✅ Custom Admin Actions for Order Management
    actions = ['confirm_orders', 'mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'cancel_orders']

    def confirm_orders(self, request, queryset):
        updated = queryset.filter(order_status='pending').update(order_status='confirmed')
        self.message_user(request, f"{updated} order(s) confirmed successfully.")
    confirm_orders.short_description = "✅ Confirm selected orders"

    def mark_as_processing(self, request, queryset):
        updated = queryset.filter(order_status='confirmed').update(order_status='processing')
        self.message_user(request, f"{updated} order(s) moved to Processing.")
    mark_as_processing.short_description = "⚙️ Mark selected orders as Processing"

    def mark_as_shipped(self, request, queryset):
        updated = queryset.filter(order_status='processing').update(order_status='shipped')
        self.message_user(request, f"{updated} order(s) marked as Shipped.")
    mark_as_shipped.short_description = "📦 Mark selected orders as Shipped"

    def mark_as_delivered(self, request, queryset):
        updated = queryset.filter(order_status='shipped').update(order_status='delivered')
        self.message_user(request, f"{updated} order(s) marked as Delivered.")
    mark_as_delivered.short_description = "🚚 Mark selected orders as Delivered"

    def cancel_orders(self, request, queryset):
        updated = queryset.exclude(order_status='delivered').update(order_status='cancelled')
        self.message_user(request, f"{updated} order(s) cancelled successfully.")
    cancel_orders.short_description = "❌ Cancel selected orders"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'total_price']
    list_filter = ['order__order_status', 'product__category']
    search_fields = ['order__order_number', 'product__name']

