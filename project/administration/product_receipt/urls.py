from django.urls import path

from . import views

app_name = 'admin_product_receipt'

urlpatterns = [
    path('', views.ProductReceiptListView.as_view(), name='product-receipt-list'),
    path('product-delete/<id>/', views.ProductReceiptDeleteView.as_view(), name='product-receipt-delete'),
    path('product-receipt-create/', views.ProductReceiptCreateView.as_view(), name='product-receipt-create'),
    path('product-receipt-item-create/<id>/', views.ProductReceiptItemCreateView.as_view(), name='product-receipt-item-create'),
    path('product-receipt-item-delete/<id>/', views.ProductReceiptItemDeleteView.as_view(), name='product-receipt-item-delete'),
    path('<id>/', views.ProductReceiptDetailView.as_view(), name='product-receipt-detail'),
]