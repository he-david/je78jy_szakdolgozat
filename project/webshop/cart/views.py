from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from .models import Cart, CartItem
from .utils import get_or_set_cart

class CartView(generic.TemplateView):
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context["cart"] = get_or_set_cart(self.request)
        return context

class RemoveFromCartView(generic.View):
    def get(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, id=kwargs['pk'])
        # Cart price
        cart = Cart.objects.get(id=cart_item.cart_id.id)
        cart.net_price -= (cart_item.product_id.net_price * cart_item.quantity * 
                                cart_item.package_type_id.quantity)
        cart.gross_price -= (cart_item.product_id.net_price * (1 + cart_item.product_id.vat/100) * cart_item.quantity * 
                            cart_item.package_type_id.quantity)
        cart_item.delete()
        cart.save()
        return redirect('webshop_cart:summary')