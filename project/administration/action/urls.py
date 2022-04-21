from django.urls import path, include

from . import views

app_name = 'admin_action'

urlpatterns = [
    path('', views.ActionListView.as_view(), name='action-list'),
    path('action-create/', views.ActionCreateView.as_view(), name='action-create'),
    path('action-delete/<int:id>', views.ActionDeleteView.as_view(), name='action-delete'),
    path('<int:id>/', views.ActionDetailView.as_view(), name='action-detail'),
]