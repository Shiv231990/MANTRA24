from .models import Category

def sidebar_categories(request):
    return {
        'all_categories': Category.objects.all()
    }