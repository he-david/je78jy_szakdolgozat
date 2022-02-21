from django.views import generic

from webshop.core.models import FAQTopic, FAQ

class HomeView(generic.TemplateView):
    template_name = 'core/index.html'

class FAQListView(generic.ListView):
    template_name = 'core/faq_list.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        qs = FAQ.objects.order_by('topic_id')
        return qs