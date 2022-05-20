from django.shortcuts import get_object_or_404, reverse
from django.views import generic

import math

from administration.admin_core.mixins import UserAccessMixin
from .forms import SalesOrderForm
from administration.invoice import utils as invoice_utils
from administration.delivery_note import utils as delivery_note_utils
from . import utils as sales_order_utils
from .models import SalesOrder
from administration.admin_core import utils as admin_utils

class SalesOrderListView(UserAccessMixin, generic.ListView):
    permission_required = 'sales_order.view_salesorder'
    template_name = 'sales_order/sales_order_list.html'
    paginate_by = 25
    ORDER_LIST = [
        'document_number_key', '-document_number_key',
        'order_date', '-order_date',
        'net_price', '-net_price',
        'gross_price', '-gross_price',
        'original_customer_name', '-original_customer_name',
        'payment_type', '-payment_type',
        'delivery_mode', '-delivery_mode',
        'status', '-status'
    ]

    def get_queryset(self):
        order_by_attr = self.request.GET.get('order_by', 'document_number_key')
        return SalesOrder.objects.all().order_by(admin_utils.get_order_attr(order_by_attr, 'document_number_key', self.ORDER_LIST))

    def get_context_data(self, **kwargs):
        context = super(SalesOrderListView, self).get_context_data(**kwargs)
        order_attr = self.request.GET.get('order_by', 'document_number_key')
        return admin_utils.order_by_context_fill(context, order_attr, self.ORDER_LIST)

class SalesOrderDetailView(UserAccessMixin, generic.UpdateView):
    permission_required = (
        'sales_order.view_salesorderitem', 'sales_order.change_salesorder',
        'delivery_note.add_deliverynote', 'invoice.add_invoice'
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