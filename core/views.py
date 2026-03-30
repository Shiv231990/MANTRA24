from django.shortcuts import render, get_object_or_404
from apps.products.models import Category


def home(request):
    """
    Homepage:
    - Displays only categories that have products
    - Prefetches related products for performance
    """

    categories = (
        Category.objects
        .prefetch_related('products')
        .filter(products__isnull=False)
        .distinct()
    )

    return render(request, 'index.html', {
        'categories': categories
    })


def category_detail(request, slug):
    """
    Category Detail Page:
    - Displays products of a specific category
    - Shows only available products
    """

    category = get_object_or_404(Category, slug=slug)

    products = (
        category.products
        .filter(available=True)
        .order_by('-created')
    )

    return render(request, 'category_detail.html', {
        'category': category,
        'products': products
    })