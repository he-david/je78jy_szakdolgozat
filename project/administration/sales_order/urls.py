from django.urls import path

from . import views

app_name = 'admin_sales_order'

urlpatterns = [
    path('', views.SalesOrderListView.as_view(), name='sales-order-list'),
    path('<id>/', views.SalesOrderDetailView.as_view(), name='sales-order-detail'),
]