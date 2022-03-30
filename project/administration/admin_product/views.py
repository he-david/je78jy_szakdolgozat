from django.shortcuts import get_object_or_404, reverse
from django.views import generic

from webshop.product.models import PackageType, Product
from administration.admin_core.mixins import StaffUserMixin
from .forms import ProductForm, ProductCreateForm, PackageForm

import math

# Product

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
        product = get_object_or_404(Product, id=self.kwargs['id'])
        product.net_price = math.floor(product.net_price/100)
        return product

    def form_valid(self, form):
        product = form.save(commit=False)
        product.net_price *= 100
        return super(ProductDetailView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin_core:admin_product:product-list')

class ProductCreateView(StaffUserMixin, generic.CreateView):
    template_name = 'admin_product/product_create.html'
    form_class = ProductCreateForm

    def form_valid(self, form):
        product = form.save(commit=False)
        product.net_price *= 100 # Az eltárolás miatt.
        product.save()
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

# Package

class PackageListView(StaffUserMixin, generic.ListView):
    template_name = 'admin_product/package_list.html'
    context_object_name = 'packages'

    def get_queryset(self):
        return PackageType.objects.all()

class PackageDetailView(StaffUserMixin, generic.UpdateView):
    template_name = 'admin_product/package_detail.html'
    context_object_name = 'package'
    form_class = PackageForm

    def get_object(self):
        return get_object_or_404(PackageType, id=self.kwargs['id'])

    def get_success_url(self):
        return reverse('admin_core:admin_product:package-list')

class PackageCreateView(StaffUserMixin, generic.CreateView):
    template_name = 'admin_product/package_create.html'
    form_class = PackageForm

    def form_valid(self, form):
        form.save()
        return super(PackageCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin_core:admin_product:package-list')

class PackageDeleteView(StaffUserMixin, generic.DeleteView):
    template_name = 'admin_product/package_delete.html'
    context_object_name = 'package'

    def get_object(self):
        return get_object_or_404(PackageType, id=self.kwargs['id'])

    def get_success_url(self):
        return reverse('admin_core:admin_product:package-list')