from .models import Cart, CartItem

def cart_context(request):
    if request.user.is_authenticated:
        try:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            total_items = sum(item.quantity for item in cart_items)
            total_price = sum(item.total_price for item in cart_items)
            return {
                'global_cart_items': cart_items,
                'global_cart_total_items': total_items,
                'global_cart_total_price': total_price
            }
        except Exception:
            pass
    return {
        'global_cart_items': [],
        'global_cart_total_items': 0,
        'global_cart_total_price': 0
    }
