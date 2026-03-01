import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from apps.orders.models import Order
from apps.cart.cart import Cart

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@csrf_exempt
def payment_verify(request):
    """
    Handles the callback from Razorpay after payment.
    """
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            # Verify the payment signature
            client.utility.verify_payment_signature(params_dict)
            
            # Update order in DB
            order = Order.objects.get(razorpay_order_id=order_id)
            order.paid = True
            order.razorpay_payment_id = payment_id
            order.save()
            
            # Clear the cart
            cart = Cart(request)
            cart.clear()

            return render(request, 'payments/success.html', {'order': order})
        except Exception as e:
            return render(request, 'payments/failure.html', {'error': str(e)})
    
    return redirect('cart:cart_detail')