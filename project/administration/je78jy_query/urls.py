from django.urls import path

from . import views

app_name = 'je78jy_query'

urlpatterns = [
    path('income-query/', views.IncomeListView.as_view(), name='income-list'),
    path('stock-movement-query/', views.StockMovementListView.as_view(), name='stock-movement-list'),
]