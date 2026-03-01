from django.shortcuts import render, get_object_or_404
from apps.products.models import Category, Product

def home(request):
    """Fetches all categories to display as large blocks on the homepage"""
    categories = Category.objects.all().prefetch_related('products')
    return render(request, 'index.html', {'categories': categories})

def category_detail(request, category_id):
    """Displays products for a specific category when a block is clicked"""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_detail.html', {
        'category': category,
        'products': products
    })