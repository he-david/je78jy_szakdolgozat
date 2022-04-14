from django.shortcuts import get_object_or_404, reverse
from django.views import generic

import math

from administration.admin_core.mixins import UserAccessMixin
from .models import DeliveryNote, DeliveryNoteItem
from .forms import DeliveryNoteForm
from . import utils

class DeliveryNoteListView(UserAccessMixin, generic.ListView):
    permission_required = 'delivery_note.view_deliverynote'
    template_name = 'delivery_note/delivery_note_list.html'
    context_object_name = 'delivery_notes'

    def get_queryset(self):
        return DeliveryNote.objects.filter(deleted=False).order_by('document_number')
    
class DeliveryNoteDetailView(UserAccessMixin, generic.UpdateView):
    permission_required = ('delivery_note.view_deliverynoteitem', 'delivery_note.change_deliverynote')
    template_name = 'delivery_note/delivery_note_detail.html'
    context_object_name = 'delivery_note'
    form_class = DeliveryNoteForm

    def get_object(self):
        delivery_note = get_object_or_404(DeliveryNote, id=self.kwargs['id'])
        delivery_note.net_price = math.floor(delivery_note.net_price/100)
        delivery_note.gross_price = math.floor(delivery_note.gross_price/100)
        return delivery_note

    def get_success_url(self):
        if self.request.method == 'POST':
            delivery_note = self.get_object()
            utils.delivery_note_completion(delivery_note, delivery_note.conn_sales_order_id)

        return reverse('admin_core:admin_delivery_note:delivery-note-list')