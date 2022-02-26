from django import forms

from webshop.cart.models import CartItem
from .models import PackageType, Product

class AddToCartForm(forms.ModelForm):
    package_type_id = forms.ModelChoiceField(queryset=PackageType.objects.none())
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = CartItem
        fields = ['quantity', 'package_type_id']

    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop('product_id')
        product = Product.objects.get(id=self.product_id)
        super().__init__(*args, **kwargs)

        self.fields['package_type_id'].queryset = product.package_type_id.all()

    def clean(self):
        product = Product.objects.get(id=self.product_id)
        quantity = self.cleaned_data['quantity']
        # TODO HEDA lehet, hogy kell még a package is ide majd
        if product.free_stock < quantity:
            raise forms.ValidationError(f"A maximális rendelkezésre álló készlet: {product.free_stock}") # TODO ez rettentően jelenik meg