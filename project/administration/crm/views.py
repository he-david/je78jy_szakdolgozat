from django.shortcuts import get_object_or_404, reverse
from django.views import generic

from administration.admin_core.mixins import UserAccessMixin
from webshop.core.models import FAQ, Contact, CustomUser, FAQTopic
from .forms import ContactForm, FaqForm, FaqTopicForm
from administration.admin_core import utils as admin_utils

# Partner

class PartnerListView(UserAccessMixin, generic.ListView):
    permission_required = 'core.view_customuser'
    template_name = 'crm/partner_list.html'
    paginate_by = 25
    ORDER_LIST = [
        'last_name', '-last_name',
        'email', '-email'
    ]

    def get_queryset(self):
        order_by_attr = self.request.GET.get('order_by', 'last_name')
        return CustomUser.objects.filter(is_staff=False).order_by(admin_utils.get_order_attr(order_by_attr, 'last_name', self.ORDER_LIST))
            
    def get_context_data(self, **kwargs):
        context = super(PartnerListView, self).get_context_data(**kwargs)
        order_attr = self.request.GET.get('order_by', 'last_name')
        return admin_utils.order_by_context_fill(context, order_attr, self.ORDER_LIST)

# Message

class MessageListView(UserAccessMixin, generic.ListView):
    permission_required = 'core.view_contact'
    template_name = 'crm/message_list.html'
    paginate_by = 25
    ORDER_LIST = [
        'last_name', '-last_name',
        'email', '-email',
        'message', '-message'
    ]

    def get_queryset(self):
        order_by_attr = self.request.GET.get('order_by', 'last_name')
        return Contact.objects.all().order_by(admin_utils.get_order_attr(order_by_attr, 'last_name', self.ORDER_LIST))

    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        order_attr = self.request.GET.get('order_by', 'last_name')
        return admin_utils.order_by_context_fill(context, order_attr, self.ORDER_LIST)

class MessageDetailView(UserAccessMixin, generic.UpdateView):
    permission_required = 'core.view_contact'
    template_name = 'crm/message_detail.html'
    context_object_name = 'message'
    form_class = ContactForm

    def get_object(self):
        return get_object_or_404(Contact, id=self.kwargs['id'])

class MessageDeleteView(UserAccessMixin, generic.DeleteView):
    permission_required = 'core.delete_contact'
    template_name = 'crm/message_delete.html'
    context_object_name = 'message'

    def get_object(self):
        return get_object_or_404(Contact, id=self.kwargs['id'])
    
    def get_success_url(self):
        return reverse('admin_core:crm:message-list')

# FAQ Topic

class FaqTopicListView(UserAccessMixin, generic.ListView):
    permission_required = 'core.view_faqtopic'
    template_name = 'crm/faq_topic_list.html'
    paginate_by = 25
    ORDER_LIST = [
        'name', '-name',
    ]

    def get_queryset(self):
        order_by_attr = self.request.GET.get('order_by', 'name')
        return FAQTopic.objects.all().order_by(admin_utils.get_order_attr(order_by_attr, 'name', self.ORDER_LIST))

    def get_context_data(self, **kwargs):
        context = super(FaqTopicListView, self).get_context_data(**kwargs)
        order_attr = self.request.GET.get('order_by', 'name')
        return admin_utils.order_by_context_fill(context, order_attr, self.ORDER_LIST)

class FaqTopicDetailView(UserAccessMixin, generic.UpdateView):
    permission_required = 'core.change_faqtopic'
    template_name = 'crm/faq_topic_detail.html'
    context_object_name = 'topic'
    form_class = FaqTopicForm

    def get_object(self):
        return get_object_or_404(FAQTopic, id=self.kwargs['id'])

    def get_success_url(self):
        return reverse('admin_core:crm:faq-topic-list')

class FaqTopicCreateView(UserAccessMixin, generic.CreateView):
    permission_required = 'core.add_faqtopic'
    template_name = 'crm/faq_topic_create.html'
    form_class = FaqTopicForm

    def form_valid(self, form):
        form.save()
        return super(FaqTopicCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin_core:crm:faq-topic-list')

class FaqTopicDeleteView(UserAccessMixin, generic.DeleteView):
    permission_required = 'core.delete_faqtopic'
    template_name = 'crm/faq_topic_delete.html'
    context_object_name = 'topic'

    def get_object(self):
        return get_object_or_404(FAQTopic, id=self.kwargs['id'])
    
    def get_success_url(self):
        return reverse('admin_core:crm:faq-topic-list')

# FAQ

class FaqListView(UserAccessMixin, generic.ListView):
    permission_required = ('core.view_faq', 'core.view_faqtopic')
    template_name = 'crm/faq_list.html'
    paginate_by = 25
    ORDER_LIST = [
        'topic_id__name', '-topic_id__name',
        'question', '-question',
        'answer', '-answer'
    ]

    def get_queryset(self):
        order_by_attr = self.request.GET.get('order_by', 'topic_id__name')
        return FAQ.objects.all().order_by(admin_utils.get_order_attr(order_by_attr, 'topic_id__name', self.ORDER_LIST))

    def get_context_data(self, **kwargs):
        context = super(FaqListView, self).get_context_data(**kwargs)
        order_attr = self.request.GET.get('order_by', 'topic_id__name')
        return admin_utils.order_by_context_fill(context, order_attr, self.ORDER_LIST)

class FaqDetailView(UserAccessMixin, generic.UpdateView):
    permission_required = ('core.change_faq', 'core.view_faqtopic')
    template_name = 'crm/faq_detail.html'
    context_object_name = 'faq'
    form_class = FaqForm

    def get_object(self):
        return get_object_or_404(FAQ, id=self.kwargs['id'])

    def get_success_url(self):
        return reverse('admin_core:crm:faq-list')

class FaqCreateView(UserAccessMixin, generic.CreateView):
    permission_required = ('core.add_faq', 'core.view_faqtopic')
    template_name = 'crm/faq_create.html'
    form_class = FaqForm

    def form_valid(self, form):
        form.save()
        return super(FaqCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin_core:crm:faq-list')

class FaqDeleteView(UserAccessMixin, generic.DeleteView):
    permission_required = 'core.delete_faq'
    template_name = 'crm/faq_delete.html'
    context_object_name = 'faq'

    def get_object(self):
        return get_object_or_404(FAQ, id=self.kwargs['id'])
    
    def get_success_url(self):
        return reverse('admin_core:crm:faq-list')