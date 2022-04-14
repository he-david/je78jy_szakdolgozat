from django import forms

from webshop.product.models import PackageType, Product

# Product

class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['free_stock'].widget.attrs['readonly'] = True
        self.fields['reserved_stock'].widget.attrs['readonly'] = True

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
    
    def clean_free_stock(self): # Így biztosan nem kaphat más értéket amikor mentésre kerül sor, mert nem a formba írt értéket kapja, hanem azt ami az adatbázisban van.
        if self.instance: 
            return self.instance.free_stock
        else: 
            return self.fields['free_stock']
        
    def clean_reserved_stock(self):
        if self.instance: 
            return self.instance.reserved_stock
        else: 
            return self.fields['reserved_stock']

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