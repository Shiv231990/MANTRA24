from django.core.management.base import BaseCommand
from apps.products.models import Category, SubCategory, Product
import random

class Command(BaseCommand):
    help = "Seed database with categories, subcategories and products"

    def handle(self, *args, **kwargs):

        categories = [
            "Medicinal Plants",
            "Herbal Powders",
            "Essential Oils",
            "Natural Honey",
            "Dry Fruits",
            "Spices",
            "Forest Fruits",
            "Natural Teas",
            "Resins & Gums",
            "Organic Seeds"
        ]

        for cat_name in categories:
            category, _ = Category.objects.get_or_create(name=cat_name)

            for i in range(1,6):
                sub_name = f"{cat_name} Sub {i}"
                subcategory, _ = SubCategory.objects.get_or_create(
                    name=sub_name,
                    category=category
                )

                for j in range(1,6):
                    Product.objects.get_or_create(
                        name=f"{sub_name} Product {j}",
                        subcategory=subcategory,
                        price=random.randint(100,500),
                        stock=50,
                        description="Premium forest product"
                    )

        self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully"))