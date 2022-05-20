from django.urls import path

from . import views

app_name = 'admin_invoice'

urlpatterns = [
    path('', views.InvoiceListView.as_view(), name='invoice-list'),
    path('<int:id>/', views.InvoiceDetailView.as_view(), name='invoice-detail'),
]