from django.urls import path
from . import views

app_name = 'webshop_product'

urlpatterns = [
    path('<slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('', views.ProductListView.as_view(), name='product-list')
]
