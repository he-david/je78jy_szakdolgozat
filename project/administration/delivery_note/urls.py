from django.urls import path

from . import views

app_name = 'admin_delivery_note'

urlpatterns = [
    path('', views.DeliveryNoteListView.as_view(), name='delivery-note-list'),
    path('<int:id>/', views.DeliveryNoteDetailView.as_view(), name='delivery-note-detail'),
]