from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', include('administration.admin_core.urls', namespace='admin_core')),
    path('', include('webshop.core.urls', namespace='webshop_core')),
    path('django_admin/', admin.site.urls),
    path('products/', include('webshop.product.urls', namespace='webshop_product')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cart/', include('webshop.cart.urls', namespace='webshop_cart')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)