from django.urls import path

from . import views

app_name = 'webshop_cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='summary'),
    path('remove-from-cart/<int:id>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('payment-personal/', views.PaymentPersonalView.as_view(), name='payment-personal'),
    path('payment-address/', views.PaymentAddressView.as_view(), name='payment-address'),
    path('payment-order-data/', views.PaymentOrderDataView.as_view(), name='payment-order-data'),
    path('payment-success/', views.PaymentSuccessView.as_view(), name='payment-success'),
]
