from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Change 'name' to 'cart_detail' to match your template line 40
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]