from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category

def product_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory') # NEW: Look for subcategory ID
    categories = Category.objects.all()
    
    context = {"categories": categories}

    # 1. Handle Search
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        context.update({"products": products, "search_query": query})
        return render(request, "products/category_detail.html", context)

    # 2. Handle Subcategory Filtering (NEW)
    if subcategory_id:
        # Assuming your Product model has a 'subcategory' field
        products = Product.objects.filter(subcategory_id=subcategory_id)
        context.update({"products": products})
        return render(request, "products/category_detail.html", context)

    # 3. Handle Category Filtering
    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=current_category)
        context.update({"category": current_category, "products": products})
        return render(request, "products/category_detail.html", context)

    return render(request, "products/product_list.html", context)

    # 3. Default Home Page: Show category blocks
    return render(request, "products/product_list.html", context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})