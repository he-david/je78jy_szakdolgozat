from django.shortcuts import get_object_or_404, reverse
from django.views import generic

from administration.admin_core.mixins import UserAccessMixin
from .forms import InvoiceForm
from .models import Invoice
from . import utils as invoice_utils
from administration.admin_core import utils as admin_utils

import math

class InvoiceListView(UserAccessMixin, generic.ListView):
    permission_required = 'invoice.view_invoice'
    template_name = 'invoice/invoice_list.html'
    paginate_by = 25
    ORDER_LIST = [
        'account_number_key', '-account_number_key',
        'creation_date', '-creation_date',
        'settlement_date', '-settlement_date',
        'debt', '-debt',
        'net_price', '-net_price',
        'gross_price', '-gross_price',
        'original_customer_name', '-original_customer_name',
        'payment_type', '-payment_type',
        'status', '-status',
        'conn_sales_order_id__document_number_key', '-conn_sales_order_id__document_number_key'
    ]

    def get_queryset(self):
        order_by_attr = self.request.GET.get('order_by', 'account_number_key')
        return Invoice.objects.all().order_by(admin_utils.get_order_attr(order_by_attr, 'account_number_key', self.ORDER_LIST))

    def get_context_data(self, **kwargs):
        context = super(InvoiceListView, self).get_context_data(**kwargs)
        order_attr = self.request.GET.get('order_by', 'account_number_key')
        return admin_utils.order_by_context_fill(context, order_attr, self.ORDER_LIST)

class InvoiceDetailView(UserAccessMixin, generic.UpdateView):
    permission_required = ('invoice.view_invoiceitem', 'invoice.change_invoice')
    template_name = 'invoice/invoice_detail.html'
    context_object_name = 'invoice'
    form_class = InvoiceForm

    def get_object(self):
        invoice = get_object_or_404(Invoice, id=self.kwargs['id'])
        invoice.net_price = math.floor(invoice.net_price/100)
        invoice.gross_price = math.floor(invoice.gross_price/100)
        return invoice

    def get_success_url(self):
        if self.request.method == 'POST':
            invoice = self.get_object()

            if 'settlement' in self.request.POST:
                invoice_utils.invoice_settlement(invoice, invoice.conn_sales_order_id)
            elif 'delete' in self.request.POST:
                invoice_utils.delete_invoice(invoice)
            elif 'cancel' in self.request.POST:
                invoice_utils.cancel_invoice(invoice, False)
        return reverse('admin_core:admin_invoice:invoice-list')