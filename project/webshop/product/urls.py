from django.urls import path
from . import views

app_name = 'webshop_product'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('action/', views.ActionProductListView.as_view(), name='action-product-list'),
    path('<slug>/', views.ProductDetailView.as_view(), name='product-detail'),
]
