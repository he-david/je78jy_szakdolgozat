from django.urls import path
from . import views

app_name = 'webshop_core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('faq/', views.FAQListView.as_view(), name='faq-list'),
    path('signup/', views.CustomSignupView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('user-orders/', views.UserOrdersView.as_view(), name='user-orders'),
    path('user-data/', views.UserDataView.as_view(), name='user-data'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
