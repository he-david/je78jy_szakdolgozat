from django.shortcuts import get_object_or_404, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from webshop.core.forms import AddressChangeForm
from webshop.core.views import UserDataView
from webshop.product import utils as product_utils
from administration.sales_order import utils as sales_order_utils
from .forms import PaymentPersonalForm, PaymentOrderDataForm
from .models import Cart, CartItem
from .utils import get_or_set_cart

import math

class CartView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['cart'] = get_or_set_cart(self.request)
        return context

class RemoveFromCartView(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, id=kwargs['id'])
        # Cart price
        cart = Cart.objects.get(id=cart_item.cart_id.id)
        cart.net_price -= math.floor(cart_item.product_id.net_price * cart_item.quantity * 
                                cart_item.package_type_id.quantity)
        cart.gross_price -= math.floor(cart_item.product_id.net_price * (1 + cart_item.product_id.vat/100) * cart_item.quantity * 
                            cart_item.package_type_id.quantity)
        cart_item.delete()
        cart.save()
        return redirect('webshop_cart:summary')

class PaymentPersonalView(LoginRequiredMixin, generic.FormView):
    template_name = 'cart/payment_personal.html'
    form_class = PaymentPersonalForm

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        
        if user.first_name is not None and user.last_name is not None:
            initial['first_name'] = user.first_name
            initial['last_name'] = user.last_name
        return initial
    
    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        return super(PaymentPersonalView, self).form_valid(form)

    def get_success_url(self):
        return reverse('webshop_cart:payment-address')

class PaymentAddressView(UserDataView):
    template_name = 'cart/payment_address.html'
    form_class = AddressChangeForm

    def get_success_url(self):
        if "back" in self.request.POST:
            return reverse('webshop_cart:payment-personal')
        return reverse("webshop_cart:payment-order-data")

class PaymentOrderDataView(LoginRequiredMixin, generic.FormView):
    template_name = 'cart/payment_order_data.html'
    form_class = PaymentOrderDataForm

    def get_context_data(self, **kwargs):
        context = super(PaymentOrderDataView, self).get_context_data(**kwargs)
        context['cart'] = get_or_set_cart(self.request)
        context['wrong_items'] = product_utils.get_product_with_less_stock(get_or_set_cart(self.request))
        return context

    def form_valid(self, form):
        self.form = form
        return super(PaymentOrderDataView, self).form_valid(form)

    def get_success_url(self):
        if "back" in self.request.POST:
            return reverse('webshop_cart:payment-address')
        else:
            # Megnézni, hogy van-e mindenből elegendő mennyiség.
            if not product_utils.get_product_with_less_stock(get_or_set_cart(self.request)):
                # Létrehozni a megrendelést
                sales_order_utils.create_sales_order(self.form, get_or_set_cart(self.request))
                return reverse('webshop_cart:payment-success')
            else:
                return reverse('webshop_cart:payment-order-data')

class PaymentSuccessView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'cart/payment_success.html'