from django import forms

from webshop.product.models import PackageType, Product

import math

# Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'producer', 'net_price', 'vat', 'description', 'free_stock',
                'reserved_stock', 'image', 'category_id', 'package_type_id', 'action_id')
        labels = {
            'name': 'Név',
            'producer': 'Gyártó',
            'net_price': 'Nettó ár',
            'vat': 'Áfa',
            'description': 'Leírás',
            'free_stock': 'Szabad készlet',
            'reserved_stock': 'Foglalt készlet',
            'image': 'Kép',
            'category_id': 'Kategória',
            'package_type_id': 'Kiszerelés',
            'action_id': 'Akció'
        }

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'producer', 'net_price', 'vat', 'description',
                'image', 'category_id', 'package_type_id', 'action_id')
        labels = {
            'name': 'Név',
            'producer': 'Gyártó',
            'net_price': 'Nettó ár',
            'vat': 'Áfa',
            'description': 'Leírás',
            'image': 'Kép',
            'category_id': 'Kategória',
            'package_type_id': 'Kiszerelés',
            'action_id': 'Akció'
        }

# Package

class PackageForm(forms.ModelForm):
    class Meta:
        model = PackageType
        fields = ('summary_name', 'display_name', 'quantity')
        labels = {
            'summary_name': 'Összefoglaló név',
            'display_name': 'Megjelenítendő név',
            'quantity': 'Mennyiség'
        }