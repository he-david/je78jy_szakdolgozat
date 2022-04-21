from django.shortcuts import get_object_or_404, reverse
from django.views import generic

import math

from administration.admin_core.mixins import UserAccessMixin
from .forms import SalesOrderForm
from administration.invoice import utils as invoice_utils
from administration.delivery_note import utils as delivery_note_utils
from . import utils as sales_order_utils
from .models import SalesOrder


class SalesOrderListView(UserAccessMixin, generic.ListView):
    permission_required = 'sales_order.view_salesorder'
    template_name = 'sales_order/sales_order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return SalesOrder.objects.filter().order_by('document_number')

class SalesOrderDetailView(UserAccessMixin, generic.UpdateView):
    permission_required = (
        'sales_order.view_salesorderitem', 'sales_order.change_salesorder',
        'delivery_note.view_deliverynote', 'invoice.view_invoice'
    )
    template_name = 'sales_order/sales_order_detail.html'
    context_object_name = 'order'
    form_class = SalesOrderForm

    def get_object(self):
        sales_order = get_object_or_404(SalesOrder, id=self.kwargs['id'])
        sales_order.net_price = math.floor(sales_order.net_price/100)
        sales_order.gross_price = math.floor(sales_order.gross_price/100)
        return sales_order

    def get_success_url(self):
        if self.request.method == 'POST':
            sales_order = self.get_object()

            if 'invoice_gen' in self.request.POST:
                invoice_utils.create_invoice(sales_order)
                return reverse('admin_core:admin_invoice:invoice-list')
            elif 'delivery_note_gen' in self.request.POST:
                delivery_note_utils.create_delivery_note(sales_order)
                return reverse('admin_core:admin_delivery_note:delivery-note-list')
            elif 'delete' in self.request.POST:
                sales_order_utils.delete_sales_order(sales_order)
            elif 'cancel' in self.request.POST:
                sales_order_utils.cancel_sales_order(sales_order)
        return reverse('admin_core:admin_sales_order:sales-order-list')