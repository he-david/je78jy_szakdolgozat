from django.urls import path
from . import views

app_name = 'webshop_core'

urlpatterns = [
    path('faq/', views.FAQListView.as_view(), name='faq-list'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('user-orders/', views.UserOrdersView.as_view(), name='user-orders'),
    path('user-data/', views.UserDataView.as_view(), name='user-data'),
    path('', views.HomeView.as_view(), name='home'),
]
