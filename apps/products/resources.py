from import_export import resources, fields
from import_export.widgets import Widget, ForeignKeyWidget
from .models import Product, Category, SubCategory

# ---------- CUSTOM WIDGET TO FIX DUPLICATES ----------
class SmartSubCategoryWidget(Widget):
    def clean(self, value, row=None, *args, **kwargs):
        subcategory_name = str(value).strip()
        category_val = str(row.get("category", "")).strip()

        if not subcategory_name or not category_val:
            return None

        # 1. Identify the parent Category (by Name or ID)
        try:
            if category_val.isdigit():
                parent_category = Category.objects.get(id=int(category_val))
            else:
                parent_category = Category.objects.get(name__iexact=category_val)
        except Category.DoesNotExist:
            raise Exception(f"Category '{category_val}' not found.")

        # 2. Find the SubCategory matching the name WITHIN that Category
        try:
            return SubCategory.objects.get(
                name__iexact=subcategory_name, 
                category=parent_category
            )
        except SubCategory.DoesNotExist:
            raise Exception(f"SubCategory '{subcategory_name}' not found under '{parent_category.name}'")
        except SubCategory.MultipleObjectsReturned:
            # This logic prevents the error you are seeing by narrowing the search
            raise Exception(f"Duplicate SubCategory '{subcategory_name}' found under '{parent_category.name}'.")

# ---------- PRODUCT RESOURCE ----------
class ProductResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')
    )

    subcategory = fields.Field(
        column_name='subcategory',
        attribute='subcategory',
        widget=SmartSubCategoryWidget()
    )

    class Meta:
        model = Product
        import_id_fields = ("name",)
        fields = ("name", "category", "subcategory", "price", "description", "is_active")
        skip_unchanged = True