from django.views import generic

import math

from administration.admin_core.mixins import UserAccessMixin
from administration.invoice.models import Invoice, InvoiceItem
from administration.product_receipt.models import ProductReceiptItem
from webshop.product.models import Product
from administration.admin_core import utils as admin_utils

class IncomeListView(UserAccessMixin, generic.ListView):
    permission_required = 'invoice.view_invoice'
    template_name = 'je78jy_query/income_list.html'
    paginate_by = 25
    ORDER_LIST = [
        'account_number_key', '-account_number_key',
        'settlement_date', '-settlement_date',
        'net_price', '-net_price',
        'gross_price', '-gross_price',
        'payment_type', '-payment_type',
        'conn_sales_order_id__document_number_key', '-conn_sales_order_id__document_number_key'
    ]

    def get_queryset(self):
        order_by_attr = self.request.GET.get('order_by', 'account_number_key')
        return Invoice.objects.filter(debt=0, deleted=False).order_by(admin_utils.get_order_attr(order_by_attr, 'account_number_key', self.ORDER_LIST))
            
    def get_context_data(self, **kwargs):
        context = super(IncomeListView, self).get_context_data(**kwargs)
        context['net_sum'] = math.floor((sum(Invoice.objects.filter(debt=0, deleted=False).values_list('net_price', flat=True)))/100)
        context['gross_sum'] = math.floor((sum(Invoice.objects.filter(debt=0, deleted=False).values_list('gross_price', flat=True)))/100)
        order_attr = self.request.GET.get('order_by', 'account_number_key')
        return admin_utils.order_by_context_fill(context, order_attr, self.ORDER_LIST)

class StockMovementListView(UserAccessMixin, generic.ListView):
    permission_required = ('product_receipt.view_productreceipt', 'product.view_product')
    template_name = 'je78jy_query/stock_movement_list.html'
    paginate_by = 25
    ORDER_LIST = [
        'name', '-name',
        'category_id', '-category_id'
    ]

    def get_queryset(self):
        order_by_attr = self.request.GET.get('order_by', 'name')
        return Product.objects.all().order_by(admin_utils.get_order_attr(order_by_attr, 'name', self.ORDER_LIST))
            
    def get_context_data(self, **kwargs):
        context = super(StockMovementListView, self).get_context_data(**kwargs)
        context['pos_stock'] = sum(ProductReceiptItem.objects.filter(product_receipt_id__status='final').values_list('quantity', flat=True))

        neg_stock_sum = 0
        items = InvoiceItem.objects.filter(invoice_id__status='completed')
        for item in items:
            neg_stock_sum += item.quantity * item.original_package_quantity
        context['neg_stock'] = neg_stock_sum
        order_attr = self.request.GET.get('order_by', 'name')
        return admin_utils.order_by_context_fill(context, order_attr, self.ORDER_LIST)
