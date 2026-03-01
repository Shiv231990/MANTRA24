def cart(request):  # The name must be 'cart'
    cart_data = request.session.get('cart', {})
    total_items = sum(cart_data.values()) if cart_data else 0
    return {'cart_total': total_items}