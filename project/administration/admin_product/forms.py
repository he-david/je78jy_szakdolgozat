from django import forms

from webshop.product.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'producer', 'net_price', 'vat', 'description', 'free_stock',
                'reserved_stock', 'image', 'category_id', 'package_type_id', 'action_id')

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'producer', 'net_price', 'vat', 'description',
                'image', 'category_id', 'package_type_id', 'action_id')