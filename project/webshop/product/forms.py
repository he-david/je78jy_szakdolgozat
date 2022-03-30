from django import forms

from webshop.cart.models import CartItem
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
        product = Product.objects.get(id=self.product_id)
        super().__init__(*args, **kwargs)

        self.fields['package_type_id'].queryset = product.package_type_id.all() # TODO HEDA ez menő

    def clean(self):
        product = Product.objects.get(id=self.product_id)
        quantity = self.cleaned_data['quantity']
        package_type = self.cleaned_data['package_type_id']

        if product.free_stock < quantity * package_type.quantity:
            raise forms.ValidationError(f"A maximális rendelkezésre álló készlet: {product.free_stock}")