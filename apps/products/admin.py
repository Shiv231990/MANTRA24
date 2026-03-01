from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Category, SubCategory, Product
from .resources import ProductResource


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SubCategoryInline]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource