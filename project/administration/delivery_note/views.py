from django.shortcuts import get_object_or_404, reverse
from django.views import generic

from administration.admin_core.mixins import StaffUserMixin
from .models import DeliveryNote, DeliveryNoteItem
from .forms import DeliveryNoteForm

class DeliveryNoteListView(StaffUserMixin, generic.ListView):
    template_name = 'delivery_note/delivery_note_list.html'
    context_object_name = 'delivery_notes'

    def get_queryset(self):
        return DeliveryNote.objects.filter(deleted=False).order_by('document_number')
    
class DeliveryNoteDetailView(StaffUserMixin, generic.UpdateView):
    template_name = 'delivery_note/delivery_note_detail.html'
    context_object_name = 'delivery_note'
    form_class = DeliveryNoteForm

    def get_object(self):
        return get_object_or_404(DeliveryNote, id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(DeliveryNoteDetailView, self).get_context_data(**kwargs)
        context['items'] = DeliveryNoteItem.objects.filter(delivery_note_id=self.kwargs['id'])
        return context

    def get_success_url(self):
        return reverse('admin_core:admin_delivery_note:delivery-note-list')