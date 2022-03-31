from django.urls import path

from . import views

app_name = 'admin_category'

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category-list'),
    path('category-delete/<id>/', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('category-create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('<id>/', views.CategoryDetailView.as_view(), name='category-detail'),
]