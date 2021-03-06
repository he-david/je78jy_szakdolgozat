from django.urls import path, include

from . import views

app_name = 'admin_core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('sales-order/', include('administration.sales_order.urls', namespace='admin_sales_order')),
    path('invoice/', include('administration.invoice.urls', namespace='admin_invoice')),
    path('delivery-note/', include('administration.delivery_note.urls', namespace='admin_delivery_note')),
    path('product-receipt/', include('administration.product_receipt.urls', namespace='admin_product_receipt')),
    path('category/', include('administration.category.urls', namespace='admin_category')),
    path('product/', include('administration.admin_product.urls', namespace='admin_product')),
    path('action/', include('administration.action.urls', namespace='admin_action')),
    path('crm/', include('administration.crm.urls', namespace='crm')),
    path('query/', include('administration.je78jy_query.urls', namespace='je78jy_query')),
    path('permission-denied/', views.PermissionDeniedView.as_view(), name='permission-denied'),
]