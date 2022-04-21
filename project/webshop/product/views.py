from django.http import Http404
from django.shortcuts import get_object_or_404, reverse
from django.views import generic
from django.db.models import Count

from webshop.cart.utils import get_or_set_cart
from .forms import AddToCartForm
from .models import Category, Product
from .utils import get_all_children

import math

class ProductListView(generic.ListView):
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = Product.objects.filter()

        try:
            category_id = self.request.GET.get('category', None)

            if category_id != None:
                category_id = (int)(category_id)
        except:
            raise Http404("Invalid category")

        if category_id:
            qs = qs.filter(category_id__in=get_all_children(category_id, True))
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

        try:
            category_id = self.request.GET.get('category', None)

            if category_id != None:
                category_id = (int)(category_id)
        except:
            raise Http404("Invalid category")

        if category_id:
            context['categories'] = Category.objects.filter(parent_id=category_id).values()
        else:
            context['categories'] = Category.objects.filter(parent_id=None).values()
        return context


class ProductDetailView(generic.FormView):
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
    form_class = AddToCartForm

    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse('webshop_cart:summary')

    def get_form_kwargs(self):
        kwargs = super(ProductDetailView, self).get_form_kwargs()
        kwargs['product_id'] = self.get_object().id
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context

    def form_valid(self, form): # TODO Lehet, vizsgálni kellene, hogy van-e elég
        cart = get_or_set_cart(self.request)
        product = self.get_object()

        item_filter = cart.items.filter(
            product_id = product,
            package_type_id = form.cleaned_data['package_type_id']
        )

        if item_filter.exists():
            item = item_filter.first()
            item.quantity += int(form.cleaned_data['quantity'])
            item.save()
            # Cart price
            cart.net_price += math.floor(product.get_net_price() * item.quantity * 
                                item.package_type_id.quantity)
            cart.gross_price += math.floor(product.get_net_price() * (1 + product.vat/100) * item.quantity * 
                                item.package_type_id.quantity)
            cart.save()
        else:
            new_item = form.save(commit=False)
            new_item.product_id = product
            new_item.cart_id = cart
            new_item.package_type_id = form.cleaned_data['package_type_id']
            new_item.quantity = form.cleaned_data['quantity']
            new_item.save()
            # Cart price
            cart.net_price += math.floor(product.get_net_price() * new_item.quantity * 
                                new_item.package_type_id.quantity)
            cart.gross_price += math.floor(product.get_net_price() * (1 + product.vat/100) * new_item.quantity * 
                                new_item.package_type_id.quantity)
            cart.save()
        return super(ProductDetailView, self).form_valid(form)


class ActionProductListView(generic.ListView):
    template_name = 'product/action_product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ActionProductListView, self).get_context_data(**kwargs)
        action_prod_count = 0

        for product in Product.objects.all():
            if product.get_action_percent() > 0:
                action_prod_count += 1
        context['action_prod_count'] = action_prod_count
        return context