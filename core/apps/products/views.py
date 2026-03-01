from django.db.models import Q

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    
    # Search logic
    query = request.GET.get('search')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'products/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })