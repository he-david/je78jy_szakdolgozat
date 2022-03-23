from django.urls import path

from . import views

app_name = 'admin_product'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('product-delete/<id>/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('product-create/', views.ProductCreateView.as_view(), name='product-create'),
    path('<id>/', views.ProductDetailView.as_view(), name='product-detail'),
]