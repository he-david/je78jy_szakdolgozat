from django.shortcuts import get_object_or_404, reverse
from django.views import generic

from administration.admin_core.mixins import UserAccessMixin
from webshop.core.models import FAQ, Contact, CustomUser, FAQTopic
from .forms import ContactForm, FaqForm, FaqTopicForm

# Partner

class PartnerListView(UserAccessMixin, generic.ListView):
    permission_required = 'core.view_customuser'
    template_name = 'crm/partner_list.html'
    context_object_name = 'partners'

    def get_queryset(self):
        return CustomUser.objects.filter(is_staff=False)

# Message

class MessageListView(UserAccessMixin, generic.ListView):
    permission_required = 'core.view_contact'
    template_name = 'crm/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Contact.objects.all()

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
    permission_required = 'core.view_contact' # TODO HEDA csere
    template_name = 'crm/faq_topic_list.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return FAQTopic.objects.all()

class FaqTopicDetailView(UserAccessMixin, generic.UpdateView):
    permission_required = 'core.view_contact' # TODO HEDA csere
    template_name = 'crm/faq_topic_detail.html'
    context_object_name = 'topic'
    form_class = FaqTopicForm

    def get_object(self):
        return get_object_or_404(FAQTopic, id=self.kwargs['id'])

    def get_success_url(self):
        return reverse('admin_core:crm:faq-topic-list')

class FaqTopicCreateView(UserAccessMixin, generic.CreateView):
    permission_required = 'product.add_packagetype' # TODO HEDA csere
    template_name = 'crm/faq_topic_create.html'
    form_class = FaqTopicForm

    def form_valid(self, form):
        form.save()
        return super(FaqTopicCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin_core:crm:faq-topic-list')

class FaqTopicDeleteView(UserAccessMixin, generic.DeleteView):
    permission_required = 'core.delete_contact' # TODO HEDA csere
    template_name = 'crm/faq_topic_delete.html'
    context_object_name = 'topic'

    def get_object(self):
        return get_object_or_404(FAQTopic, id=self.kwargs['id'])
    
    def get_success_url(self):
        return reverse('admin_core:crm:faq-topic-list')

# FAQ

class FaqListView(UserAccessMixin, generic.ListView):
    permission_required = 'core.view_contact' # TODO HEDA csere
    template_name = 'crm/faq_list.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        return FAQ.objects.all()

class FaqDetailView(UserAccessMixin, generic.UpdateView):
    permission_required = 'core.view_contact' # TODO HEDA csere
    template_name = 'crm/faq_detail.html'
    context_object_name = 'faq'
    form_class = FaqForm

    def get_object(self):
        return get_object_or_404(FAQ, id=self.kwargs['id'])

    def get_success_url(self):
        return reverse('admin_core:crm:faq-list')

class FaqCreateView(UserAccessMixin, generic.CreateView):
    permission_required = 'product.add_packagetype' # TODO HEDA csere
    template_name = 'crm/faq_create.html'
    form_class = FaqForm

    def form_valid(self, form):
        form.save()
        return super(FaqCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin_core:crm:faq-list')

class FaqDeleteView(UserAccessMixin, generic.DeleteView):
    permission_required = 'core.delete_contact' # TODO HEDA csere
    template_name = 'crm/faq_delete.html'
    context_object_name = 'faq'

    def get_object(self):
        return get_object_or_404(FAQ, id=self.kwargs['id'])
    
    def get_success_url(self):
        return reverse('admin_core:crm:faq-list')

# TODO HEDA jogkör teszt.