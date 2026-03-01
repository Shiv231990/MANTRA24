from .models import Category

def categories(request):
    return {
        'categories': Category.objects.filter().order_by('name')
    }
