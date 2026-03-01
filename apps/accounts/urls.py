from django.urls import path
from . import views

# This registered namespace is required for your templates
app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    # Ensure this name matches what line 64 of base.html is looking for
    path('logout/', views.logout_view, name='logout'),
]