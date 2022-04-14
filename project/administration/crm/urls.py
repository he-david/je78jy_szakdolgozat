from django.urls import path

from . import views

app_name = 'crm'

urlpatterns = [
    # Partner
    path('partner-list/', views.PartnerListView.as_view(), name='admin-partner-list'),
    # Message
    path('message-list/', views.MessageListView.as_view(), name='message-list'),
    path('message_detail/<int:id>/', views.MessageDetailView.as_view(), name='message-detail'),
    path('message-delete/<int:id>/', views.MessageDeleteView.as_view(), name='message-delete'),
    # FAQ Topic
    path('faq-topic-list/', views.FaqTopicListView.as_view(), name='faq-topic-list'),
    path('faq-topic-create/', views.FaqTopicCreateView.as_view(), name='faq-topic-create'),
    path('faq-topic-detail/<int:id>/', views.FaqTopicDetailView.as_view(), name='faq-topic-detail'),
    path('faq-topic-delete/<int:id>/', views.FaqTopicDeleteView.as_view(), name='faq-topic-delete'),
    # FAQ
    path('faq-list/', views.FaqListView.as_view(), name='faq-list'),
    path('faq-create/', views.FaqCreateView.as_view(), name='faq-create'),
    path('faq-detail/<int:id>/', views.FaqDetailView.as_view(), name='faq-detail'),
    path('faq-delete/<int:id>/', views.FaqDeleteView.as_view(), name='faq-delete'),
]