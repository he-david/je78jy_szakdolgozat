from django.http import Http404
from django.shortcuts import get_object_or_404, reverse, redirect
from django.views import generic

from administration.admin_core.mixins import UserAccessMixin
from .models import ProductReceipt, ProductReceiptItem
from .forms import ProductReceiptForm, ProductReceiptItemForm
from . import utils as receipt_utils

# ProductReceipt

class ProductReceiptListView(UserAccessMixin, generic.ListView):
    permission_required = ('product_receipt.view_productreceipt', 'product_receipt.add_productreceipt')
    template_name = 'product_receipt/product_receipt_list.html'
    context_object_name = 'receipts'

    def get_queryset(self):
        return ProductReceipt.objects.all()

class ProductReceiptDetailView(UserAccessMixin, generic.UpdateView):
    permission_required = ('product_receipt.view_productreceiptitem', 'product_receipt.change_productreceipt')
    template_name = 'product_receipt/product_receipt_detail.html'
    context_object_name = 'receipt'
    form_class = ProductReceiptForm

    def get_object(self):
        return get_object_or_404(ProductReceipt, id=self.kwargs['id'])
    
    def get_context_data(self, **kwargs):
        context = super(ProductReceiptDetailView, self).get_context_data(**kwargs)
        context['items'] = ProductReceiptItem.objects.filter(product_receipt_id=self.kwargs['id'])
        return context

    def get_success_url(self):
        if self.request.method == 'POST':
            receipt = self.get_object()

            if 'final' in self.request.POST:
                receipt_utils.finalize_product_receipt(receipt)
        return reverse('admin_core:admin_product_receipt:product-receipt-list')

class ProductReceiptCreateView(UserAccessMixin, generic.View):
    permission_required = (
        'product_receipt.add_productreceipt', 'product_receipt.change_productreceipt',
        'product_receipt.view_productreceiptitem'
    )

    def get(self, *args, **kwargs):
        receipt = receipt_utils.create_product_receipt()
        return redirect(reverse("admin_core:admin_product_receipt:product-receipt-detail", kwargs={"id": receipt.id}))

class ProductReceiptDeleteView(UserAccessMixin, generic.DeleteView):
    permission_required = 'product_receipt.delete_productreceipt'
    template_name = 'product_receipt/product_receipt_delete.html'
    context_object_name = 'receipt'

    def get_object(self):
        return get_object_or_404(ProductReceipt, id=self.kwargs['id'])

    def get_success_url(self):
        return reverse('admin_core:admin_product_receipt:product-receipt-list')

# ProductReceiptItem

class ProductReceiptItemCreateView(UserAccessMixin, generic.CreateView):
    permission_required = 'product_receipt.add_productreceiptitem'
    template_name = 'product_receipt/product_receipt_item_create.html'
    form_class = ProductReceiptItemForm

    def get_context_data(self, **kwargs):
        context = super(ProductReceiptItemCreateView, self).get_context_data(**kwargs)
        receipt = ProductReceipt.objects.get(id=self.kwargs['id'])
        context['receipt'] = receipt

        # Ha a bizonylat már végleges
        if receipt.status == 'final':
            raise Http404('A bizonylat már végleges.')
        return context

    def form_valid(self, form):
        receipt_item = form.save(commit=False)
        receipt_utils.create_product_receipt_item(receipt_item, self.kwargs['id'])
        return super(ProductReceiptItemCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("admin_core:admin_product_receipt:product-receipt-detail", kwargs={"id": self.kwargs['id']})

class ProductReceiptItemDeleteView(UserAccessMixin, generic.View):
    permission_required = 'product_receipt.delete_productreceiptitem'
    
    def get(self, *args, **kwargs):
        receipt_item = get_object_or_404(ProductReceiptItem, id=kwargs['id'])
        receipt = receipt_item.product_receipt_id

        # Ha a bizonylat már végleges
        if receipt.status == 'final':
            raise Http404('A bizonylat már végleges.')
        receipt_utils.change_product_receipt_sum_quantity(receipt, -receipt_item.quantity)
        receipt_item.delete()
        return redirect(reverse("admin_core:admin_product_receipt:product-receipt-detail", kwargs={"id": receipt.id}))