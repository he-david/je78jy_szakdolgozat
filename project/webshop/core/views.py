from django.views import generic

from .models import FAQ
from .forms import CustomUserCreationForm
from administration.sales_order.models import SalesOrder

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

class UserProfileView(generic.TemplateView):
    template_name = 'core/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['orders'] = SalesOrder.objects.filter(customer_id=self.request.user, deleted=False) # TODO lehet, hogy kezelni kell, ha nincs belépve
        return context