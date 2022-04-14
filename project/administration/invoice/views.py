from django.shortcuts import get_object_or_404, reverse
from django.views import generic

from administration.admin_core.mixins import UserAccessMixin
from .forms import InvoiceForm
from .models import Invoice, InvoiceItem
from . import utils

import math

class InvoiceListView(UserAccessMixin, generic.ListView):
    permission_required = 'invoice.view_invoice'
    template_name = 'invoice/invoice_list.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return Invoice.objects.filter(deleted=False).order_by('account_number')

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
            utils.invoice_settlement(invoice, invoice.conn_sales_order_id)
            
        return reverse('admin_core:admin_invoice:invoice-list')