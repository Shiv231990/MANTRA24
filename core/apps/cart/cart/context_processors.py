from .cart import Cart

def cart(request):
    cart_obj = Cart(request)
    return {
        'cart': cart_obj,
        'cart_count': sum(item['quantity'] for item in cart_obj)
    }