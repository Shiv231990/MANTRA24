from django.urls import path
from . import views

# This 'app_name' fixes the 'orders' is not a registered namespace error
app_name = 'orders'

urlpatterns = [
    # This 'name' must match the link in your cart/detail.html template
    path('checkout/', views.checkout, name='checkout'),
]