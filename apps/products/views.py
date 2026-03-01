from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.prefetch_related("products")

    context = {
        "products": products,
        "categories": categories,
    }
    return render(request, "products/product_list.html", context)

# NEW: View to display full product details and images
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})