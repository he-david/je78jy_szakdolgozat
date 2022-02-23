from django.urls import path
from . import views

app_name = 'webshop_core'

urlpatterns = [
    path('faq/', views.FAQListView.as_view(), name='faq-list'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('', views.HomeView.as_view(), name='home'),
]
