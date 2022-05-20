from django.shortcuts import get_object_or_404, reverse
from django.views import generic

import math

from administration.admin_core.mixins import UserAccessMixin
from .models import DeliveryNote
from .forms import DeliveryNoteForm
from . import utils as delivery_note_utils
from administration.admin_core import utils as admin_utils

class DeliveryNoteListView(UserAccessMixin, generic.ListView):
    permission_required = 'delivery_note.view_deliverynote'
    template_name = 'delivery_note/delivery_note_list.html'
    paginate_by = 25
    ORDER_LIST = [
        'document_number_key', '-document_number_key',
        'completion_date', '-completion_date',
        'net_price', '-net_price',
        'gross_price', '-gross_price',
        'original_customer_name', '-original_customer_name',
        'payment_type', '-payment_type',
        'delivery_mode', '-delivery_mode',
        'status', '-status',
        'conn_sales_order_id__document_number_key', '-conn_sales_order_id__document_number_key'
    ]

    def get_queryset(self):
        order_by_attr = self.request.GET.get('order_by', 'document_number_key')
        return DeliveryNote.objects.all().order_by(admin_utils.get_order_attr(order_by_attr, 'document_number_key', self.ORDER_LIST))

    def get_context_data(self, **kwargs):
        context = super(DeliveryNoteListView, self).get_context_data(**kwargs)
        order_attr = self.request.GET.get('order_by', 'document_number_key')
        return admin_utils.order_by_context_fill(context, order_attr, self.ORDER_LIST)
    
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

            if 'completion' in self.request.POST:
                delivery_note_utils.delivery_note_completion(delivery_note, delivery_note.conn_sales_order_id)
            elif 'delete' in self.request.POST:
                delivery_note_utils.delete_delivery_note(delivery_note)
            elif 'cancel' in self.request.POST:
                delivery_note_utils.cancel_delivery_note(delivery_note)

        return reverse('admin_core:admin_delivery_note:delivery-note-list')