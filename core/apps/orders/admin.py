from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'email', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    
    # Custom Action to mark orders as paid
    actions = ['mark_as_paid']

    def mark_as_paid(self, request, queryset):
        queryset.update(paid=True)
    mark_as_paid.short_description = "Mark selected orders as paid"