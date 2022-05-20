from django import forms

from webshop.cart.models import CartItem, Cart
from .models import Product

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ('quantity', 'package_type_id')
        labels = {
            'quantity': 'Mennyiség',
            'package_type_id': 'Kiszerelés'
        }

    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop('product_id')
        self.user = kwargs.pop('user')
        product = Product.objects.get(id=self.product_id)
        super().__init__(*args, **kwargs)

        self.fields['package_type_id'].queryset = product.package_type_id.all()

    def clean(self):
        product = Product.objects.get(id=self.product_id)
        quantity = self.cleaned_data['quantity']

        if quantity <= 0:
            raise forms.ValidationError(f"A kiválasztott mennyiség nem lehet 1-nél kisebb.")

        package_type = self.cleaned_data['package_type_id']
        cart = Cart.objects.filter(customer_id=self.user).first()
        cart_items = CartItem.objects.filter(cart_id=cart, product_id=product)
        cart_product_count = 0

        for item in cart_items:
            cart_product_count += item.get_full_quantity()

        if product.free_stock < (quantity * package_type.quantity + cart_product_count):
            raise forms.ValidationError(f"A maximális rendelkezésre álló készlet: {product.free_stock}")