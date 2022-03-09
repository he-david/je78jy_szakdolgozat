from django.urls import path, include

from . import views


app_name = 'admin_core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('sales-order/', include('administration.sales_order.urls', namespace='admin_sales_order')),
]