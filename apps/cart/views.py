import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from apps.products.models import Product
from django.contrib import messages  # ✅ Add this import

def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    
    # ✅ FIX: Fetch the product so the 'product' variable is defined
    product = get_object_or_404(Product, id=product_id)
    
    quantity = int(request.POST.get('quantity', 1))
    
    # Add/Update cart logic
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    
    request.session['cart'] = cart
    request.session.modified = True 
    
    # ✅ Now 'product' is defined and this will work
    messages.success(request, f"{product.name} added to your Mantra24 cart!")
    
    return redirect('cart:cart_detail') 

def cart_remove(request, product_id):
    """Removes a specific product from the session-based cart."""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart:cart_detail')

def cart_detail(request):
    """Calculates totals and prepares cart items for the detail template."""
    cart = request.session.get('cart', {})
    cart_items = []
    total_amount = 0 # ✅ Matches {{ total_amount }} in your template

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = product.price * quantity
            total_amount += item_total

            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': product.price,
                'total': item_total # ✅ Matches item.total in your template
            })

        except Product.DoesNotExist:
            continue

    return render(request, 'cart/detail.html', {
        'cart_items': cart_items,   # ✅ Matches {% for item in cart_items %}
        'total_amount': total_amount 
    })

def checkout(request):
    """Generates a Razorpay order based on the current session cart."""
    cart = request.session.get('cart', {})
    total_amount = 0
    
    if cart:
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        for product in products:
            quantity = cart.get(str(product.id))
            total_amount += product.price * quantity

    razorpay_order_id = None
    amount_in_paise = 0
    
    if total_amount > 0:
        # Amount must be converted to paise for Razorpay (1 INR = 100 Paise)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        amount_in_paise = int(total_amount * 100)
        data = {
            "amount": amount_in_paise,
            "currency": "INR",
            "payment_capture": "1"
        }
        # Create order on server side to prevent client-side tampering
        razorpay_order = client.order.create(data=data)
        razorpay_order_id = razorpay_order['id']

    context = {
        "total_amount": total_amount,
        "razorpay_order_id": razorpay_order_id,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "amount_in_paise": amount_in_paise,
    }
    return render(request, "orders/checkout.html", context)