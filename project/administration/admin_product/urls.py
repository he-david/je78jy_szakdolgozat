from django.urls import path

from . import views

app_name = 'admin_product'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('product-delete/<int:id>/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('product-create/', views.ProductCreateView.as_view(), name='product-create'),
    path('package/', views.PackageListView.as_view(), name='package-list'),
    path('package/package-create/', views.PackageCreateView.as_view(), name='package-create'),
    path('package/package-delete/<int:id>', views.PackageDeleteView.as_view(), name='package-delete'),
    path('package/<int:id>/', views.PackageDetailView.as_view(), name='package-detail'),
    path('<int:id>/', views.ProductDetailView.as_view(), name='product-detail'),
]