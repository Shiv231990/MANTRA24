from django.shortcuts import render
from apps.cart.cart import Cart
from django.conf import settings

def checkout(request):
    cart = Cart(request)
    # Razorpay integration parameters
    context = {
        'cart': cart,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'total_amount': cart.get_total_price() * 100, # In paise
        'currency': 'INR'
    }
    return render(request, 'orders/checkout.html', context)