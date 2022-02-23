from django.views import generic

from .models import FAQ
from .forms import CustomUserCreationForm

class HomeView(generic.TemplateView):
    template_name = 'core/index.html'

class FAQListView(generic.ListView):
    template_name = 'core/faq_list.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        qs = FAQ.objects.order_by('topic_id')
        return qs

class SignupView(generic.edit.CreateView):
    form_class = CustomUserCreationForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'