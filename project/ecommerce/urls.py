from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('webshop.product.urls', namespace='webshop_product')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', include('django.contrib.auth.urls')),
    path('', include('webshop.core.urls', namespace='webshop_core')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)