import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from apps.products.models import Product


def initiate_payment(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart:cart_detail')

    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            total_price += product.price * quantity
        except Product.DoesNotExist:
            continue

    amount_paise = int(total_price * 100)

    try:
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        payment_order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": "1"
        })

    except Exception as e:
        return render(request, "payments/error.html", {"error": str(e)})

    context = {
        "razorpay_order_id": payment_order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount_paise": amount_paise,
        "total_price": total_price,
        "currency": "INR"
    }

    return render(request, "orders/checkout.html", context)


@csrf_exempt
def verify_payment(request):

    if request.method == "POST":

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)

            # ✅ Payment verified → clear cart
            request.session['cart'] = {}
            request.session.modified = True

            return render(request, "payments/success.html")

        except:
            return render(request, "payments/failure.html")

    return redirect('cart:cart_detail')
