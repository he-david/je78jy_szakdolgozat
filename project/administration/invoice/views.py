from django.shortcuts import get_object_or_404, reverse
from django.views import generic

from administration.admin_core.mixins import StaffUserMixin
from .forms import InvoiceForm
from .models import Invoice, InvoiceItem
from . import utils

class InvoiceListView(StaffUserMixin, generic.ListView):
    template_name = 'invoice/invoice_list.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return Invoice.objects.filter(deleted=False).order_by('account_number')

class InvoiceDetailView(StaffUserMixin, generic.UpdateView):
    template_name = 'invoice/invoice_detail.html'
    context_object_name = 'invoice'
    form_class = InvoiceForm

    def get_object(self):
        return get_object_or_404(Invoice, id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        context['items'] = InvoiceItem.objects.filter(invoice_id=self.kwargs['id'])
        return context

    def get_success_url(self):
        if self.request.method == 'POST':
            invoice = self.get_object()
            utils.invoice_settlement(invoice, invoice.conn_sales_order_id)
            
        return reverse('admin_core:admin_invoice:invoice-list')