from django import forms

from .models import ProductReceipt, ProductReceiptItem

class ProductReceiptForm(forms.ModelForm):
    class Meta:
        model = ProductReceipt
        fields = ('status', 'finalization_date', 'document_number', 'sum_quantity')

class ProductReceiptItemForm(forms.ModelForm):
    class Meta:
        model = ProductReceiptItem
        fields = ('quantity', 'product_id')