from django.http import Http404
from django.shortcuts import get_object_or_404, reverse
from django.views import generic

import math

from webshop.product.models import PackageType, Product
from administration.admin_core.mixins import UserAccessMixin
from .forms import ProductForm, ProductCreateForm, PackageForm
from administration.admin_core import utils as admin_utils

# Product

class ProductListView(UserAccessMixin, generic.ListView):
    permission_required = ('product.view_product', 'product.view_category', 'product.view_packagetype')
    template_name = 'admin_product/product_list.html'
    paginate_by = 25
    ORDER_LIST = [
        'name', '-name',
        'producer', '-producer'
        'net_price', '-net_price',
        'vat', '-vat',
        'free_stock', '-free_stock',
        'reserved_stock', '-reserved_stock',
    ]

    def get_queryset(self):
        order_by_attr = self.request.GET.get('order_by', 'name')
        return Product.objects.all().order_by(admin_utils.get_order_attr(order_by_attr, 'name', self.ORDER_LIST))

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        order_attr = self.request.GET.get('order_by', 'name')
        return admin_utils.order_by_context_fill(context, order_attr, self.ORDER_LIST)

class ProductDetailView(UserAccessMixin, generic.UpdateView):
    permission_required = (
        'product.change_product', 'product.view_category',
        'product.view_packagetype', 'product.view_action'
    )
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
        product.save()
        return super(ProductDetailView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin_core:admin_product:product-list')

class ProductCreateView(UserAccessMixin, generic.CreateView):
    permission_required = (
        'product.add_product', 'product.view_category',
        'product.view_packagetype', 'product.view_action'
    )
    template_name = 'admin_product/product_create.html'
    form_class = ProductCreateForm

    def form_valid(self, form):
        product = form.save(commit=False)
        product.net_price *= 100 # Az eltárolás miatt.
        product.save()
        return super(ProductCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin_core:admin_product:product-list')

class ProductDeleteView(UserAccessMixin, generic.DeleteView):
    permission_required = 'product.delete_product'
    template_name = 'admin_product/product_delete.html'
    context_object_name = 'product'

    def get_object(self):
        product = get_object_or_404(Product, id=self.kwargs['id'])

        # Linkről törlés elleni védelem
        if not product.has_no_open_document():
            raise Http404(f"A/az {product.name} nevű termékhez tartozik folyamatban levő bizonylat, ezért nem törölhető.")
        return product
    
    def get_success_url(self):
        return reverse('admin_core:admin_product:product-list')

# Package

class PackageListView(UserAccessMixin, generic.ListView):
    permission_required = 'product.view_packagetype'
    template_name = 'admin_product/package_list.html'
    paginate_by = 25
    ORDER_LIST = [
        'summary_name', '-summary_name',
        'display_name', '-display_name',
        'quantity', '-quantity'
    ]

    def get_queryset(self):
        order_by_attr = self.request.GET.get('order_by', 'display_name')
        return PackageType.objects.all().order_by(admin_utils.get_order_attr(order_by_attr, 'display_name', self.ORDER_LIST))
            
    def get_context_data(self, **kwargs):
        context = super(PackageListView, self).get_context_data(**kwargs)
        order_attr = self.request.GET.get('order_by', 'display_name')
        return admin_utils.order_by_context_fill(context, order_attr, self.ORDER_LIST)

class PackageDetailView(UserAccessMixin, generic.UpdateView):
    permission_required = 'product.change_packagetype'
    template_name = 'admin_product/package_detail.html'
    context_object_name = 'package'
    form_class = PackageForm

    def get_object(self):
        return get_object_or_404(PackageType, id=self.kwargs['id'])

    def get_success_url(self):
        return reverse('admin_core:admin_product:package-list')

class PackageCreateView(UserAccessMixin, generic.CreateView):
    permission_required = 'product.add_packagetype'
    template_name = 'admin_product/package_create.html'
    form_class = PackageForm

    def form_valid(self, form):
        form.save()
        return super(PackageCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin_core:admin_product:package-list')

class PackageDeleteView(UserAccessMixin, generic.DeleteView):
    permission_required = 'product.delete_packagetype'
    template_name = 'admin_product/package_delete.html'
    context_object_name = 'package'

    def get_object(self):
        package_type = get_object_or_404(PackageType, id=self.kwargs['id'])
        
        # Linkről törlés elleni védelem
        if not package_type.is_deletable():
            raise Http404(f"Létezik olyan termék amely rendelkezik a/az {package_type.display_name} nevű kiszereléssel, ezért nem törölhető.")
        return package_type

    def get_success_url(self):
        return reverse('admin_core:admin_product:package-list')