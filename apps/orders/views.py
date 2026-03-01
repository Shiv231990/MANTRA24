import razorpay
from django.conf import settings
from django.shortcuts import render
from apps.products.models import Product

def cart_detail(request):
    """View to display the items in the shopping cart and the total amount."""
    cart = request.session.get('cart', {})
    cart_items = []
    total_amount = 0

    if cart:
        # Fetch products in bulk for efficiency
        products = Product.objects.filter(id__in=cart.keys())
        for product in products:
            quantity = cart.get(str(product.id))
            item_total = product.price * quantity
            total_amount += item_total
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total,
            })

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount, # ✅ Fixes the missing total on the cart page
    }
    return render(request, 'cart/cart_detail.html', context)

def checkout(request):
    """View to handle the checkout process and Razorpay order creation."""
    # 1. Get Cart from Session
    cart = request.session.get('cart', {})
    total_amount = 0
    
    # 2. Calculate Total from Session Data
    if cart:
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        for product in products:
            quantity = cart.get(str(product.id))
            total_amount += product.price * quantity

    # 3. Handle Razorpay if cart is not empty
    razorpay_order_id = None
    amount_in_paise = 0
    
    if total_amount > 0:
        # Razorpay expects amount in paise (1 INR = 100 paise)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        amount_in_paise = int(total_amount * 100)
        data = {
            "amount": amount_in_paise,
            "currency": "INR",
            "payment_capture": "1"
        }
        # Create the order on Razorpay servers to prevent tampering
        razorpay_order = client.order.create(data=data)
        razorpay_order_id = razorpay_order['id']

    context = {
        "total_amount": total_amount,
        "razorpay_order_id": razorpay_order_id,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "amount_in_paise": amount_in_paise,
    }
    return render(request, "orders/checkout.html", context)