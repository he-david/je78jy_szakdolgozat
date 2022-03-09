from django.urls import path

from . import views

app_name = 'webshop_cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='summary'),
    path('remove-from-cart/<pk>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
]
