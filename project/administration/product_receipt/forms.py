from django import forms

from .models import ProductReceipt, ProductReceiptItem

class ProductReceiptForm(forms.ModelForm):
    class Meta:
        model = ProductReceipt
        fields = ('status', 'finalization_date', 'document_number', 'sum_quantity')
        labels = {
            'status': 'Státusz',
            'finalization_date': 'Veglegesítés dátum',
            'document_number': 'Bizonylatszám',
            'sum_quantity': 'Összes mennyiség'
        }

class ProductReceiptItemForm(forms.ModelForm):
    class Meta:
        model = ProductReceiptItem
        fields = ('quantity', 'product_id')
        labels = {
            'quantity': 'Mennyiség',
            'product_id': 'Termék'
        }