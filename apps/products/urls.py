from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    # This URL captures the Product ID (pk) to show specific info
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]