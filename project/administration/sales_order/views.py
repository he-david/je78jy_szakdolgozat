from django.shortcuts import get_object_or_404, reverse
from django.views import generic

from administration.admin_core.mixins import StaffUserMixin
from .models import SalesOrder, SalesOrderItem
from .forms import SalesOrderForm

class SalesOrderListView(StaffUserMixin, generic.ListView):
    template_name = 'sales_order/sales_order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return SalesOrder.objects.filter(deleted=False).order_by('document_number')

class SalesOrderDetailView(StaffUserMixin, generic.UpdateView):
    template_name = 'sales_order/sales_order_detail.html'
    context_object_name = 'order'
    form_class = SalesOrderForm

    def get_object(self):
        return get_object_or_404(SalesOrder, id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(SalesOrderDetailView, self).get_context_data(**kwargs)
        context['items'] = SalesOrderItem.objects.filter(sales_order_id=self.kwargs['id'])
        return context

    def get_success_url(self):
        return reverse('admin_core:admin_sales_order:sales-order-list')