import os
import django
import requests
from django.core.files.base import ContentFile

# 1. Setup Django environment first
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv('DJANGO_SETTINGS_MODULE', 'core.settings.dev'))
django.setup()

# 2. Import models ONLY after setup is complete
from apps.products.models import Category, Product

def run():
    # Create Categories
    electronics, _ = Category.objects.get_or_create(name="Electronics", slug="electronics")
    fashion, _ = Category.objects.get_or_create(name="Fashion", slug="fashion")

    # Create Dummy Products
    products = [
        {
            "name": "Mantra Wireless Headphones",
            "price": 4999,
            "category": electronics,
            "desc": "Premium noise cancelling headphones."
        },
        {
            "name": "Urban Explorer Jacket",
            "price": 2499,
            "category": fashion,
            "desc": "Water-resistant stylish windbreaker."
        },
        {
            "name": "Minimalist Quartz Watch",
            "price": 3200,
            "category": fashion,
            "desc": "Elegant timepiece for every occasion."
        }
    ]

    for p in products:
        product, created = Product.objects.get_or_create(
            name=p['name'],
            defaults={'price': p['price'], 'category': p['category'], 'description': p['desc'], 'stock': 10}
        )
        
        if created:
            try:
                response = requests.get("https://via.placeholder.com/300", timeout=5)
                if response.status_code == 200:
                    product.image.save(f"{p['name']}.jpg", ContentFile(response.content), save=True)
            except Exception as e:
                print(f"Could not download image for {p['name']}: {e}")

    print("Seeding complete!")

if __name__ == "__main__":
    run()
