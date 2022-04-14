from django.views import generic
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from .models import FAQ, Address
from .forms import AddressChangeForm, ContactForm, CustomLoginForm, CustomUserCreationForm
from administration.sales_order.models import SalesOrder

class HomeView(generic.TemplateView):
    template_name = 'core/index.html'

class FAQListView(generic.ListView):
    template_name = 'core/faq_list.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        qs = FAQ.objects.order_by('topic_id')
        return qs

class CustomSignupView(generic.edit.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse("webshop_core:login")

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'registration/login.html'

class UserOrdersView(LoginRequiredMixin, generic.ListView):
    template_name = 'core/user_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        qs = SalesOrder.objects.filter(customer_id=self.request.user, deleted=False)
        return qs

class UserDataView(LoginRequiredMixin, generic.FormView):
    template_name = 'core/user_data.html'
    form_class = AddressChangeForm

    def get_initial(self):
        initial = super().get_initial()
        address = Address.objects.filter(customer_id=self.request.user).first()
        
        if address is not None:
            initial['zip_code'] = address.zip_code
            initial['city'] = address.city
            initial['street_name'] = address.street_name
            initial['house_number'] = address.house_number
        return initial
    
    def form_valid(self, form):
        address = Address.objects.filter(customer_id=self.request.user).first()

        if address is not None:
            address.zip_code = form.cleaned_data['zip_code']
            address.city = form.cleaned_data['city']
            address.street_name = form.cleaned_data['street_name']
            address.house_number = form.cleaned_data['house_number']
            address.save()
        else:
            new_address = form.save(commit=False)
            new_address.customer_id = self.request.user
            new_address.save()
        return super(UserDataView, self).form_valid(form)

    def get_success_url(self):
        return reverse("webshop_core:user-data")

class ContactView(generic.FormView):
    template_name = 'core/contact.html'
    form_class = ContactForm

    def get_initial(self):
        initial = super(ContactView, self).get_initial()
        user = self.request.user

        if user:
            initial['first_name'] = user.first_name
            initial['last_name'] = user.last_name
            initial['email'] = user.email
        return initial

    def form_valid(self, form):
        form.save()
        return super(ContactView, self).form_valid(form)

    def get_success_url(self):
        return reverse('webshop_core:contact')