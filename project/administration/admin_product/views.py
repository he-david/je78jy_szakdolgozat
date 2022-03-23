from django.shortcuts import get_object_or_404, reverse
from django.views import generic

from webshop.product.models import Product
from administration.admin_core.mixins import StaffUserMixin
from .forms import ProductForm, ProductCreateForm

class ProductListView(StaffUserMixin, generic.ListView):
    template_name = 'admin_product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all() # TODO HEDA valami alapján jó lenne rendezni.

class ProductDetailView(StaffUserMixin, generic.UpdateView):
    template_name = 'admin_product/product_detail.html'
    context_object_name = 'product'
    form_class = ProductForm

    def get_object(self):
        return get_object_or_404(Product, id=self.kwargs['id'])

    def get_success_url(self):
        return reverse('admin_core:admin_product:product-list')

class ProductCreateView(StaffUserMixin, generic.CreateView):
    template_name = 'admin_product/product_create.html'
    form_class = ProductCreateForm

    def form_valid(self, form):
        form.save()
        return super(ProductCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin_core:admin_product:product-list')

class ProductDeleteView(StaffUserMixin, generic.DeleteView):
    template_name = 'admin_product/product_delete.html'
    context_object_name = 'product'

    def get_object(self):
        return get_object_or_404(Product, id=self.kwargs['id'])
    
    def get_success_url(self):
        return reverse('admin_core:admin_product:product-list')