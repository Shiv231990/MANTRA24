from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# ✅ This will now work once views.py is moved out of the templates folder
from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ✅ Main Homepage
    path('', views.home, name='home'), 
     path('category/<slug:slug>/', views.category_detail, name='category_detail'),

    # API paths
    path('api/products/', include('apps.products.urls')), 
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/cart/', include('apps.cart.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/payments/', include('apps.payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)