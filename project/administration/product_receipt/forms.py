from django import forms

from .models import ProductReceipt, ProductReceiptItem

class ProductReceiptForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductReceiptForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['disabled'] = True
        self.fields['finalization_date'].widget.attrs['readonly'] = True
        self.fields['document_number'].widget.attrs['readonly'] = True
        self.fields['sum_quantity'].widget.attrs['readonly'] = True

    class Meta:
        model = ProductReceipt
        fields = ('status', 'finalization_date', 'document_number', 'sum_quantity')
        labels = {
            'status': 'Státusz',
            'finalization_date': 'Veglegesítés dátum',
            'document_number': 'Bizonylatszám',
            'sum_quantity': 'Összes mennyiség'
        }
    
    def clean_status(self): # Így biztosan nem kaphat más értéket amikor mentésre kerül sor.
        if self.instance: 
            return self.instance.status
        else: 
            return self.fields['status']
        
    def clean_finalization_date(self):
        if self.instance: 
            return self.instance.finalization_date
        else: 
            return self.fields['finalization_date']

    def clean_document_number(self):
        if self.instance: 
            return self.instance.document_number
        else: 
            return self.fields['document_number']
        
    def clean_sum_quantity(self):
        if self.instance: 
            return self.instance.sum_quantity
        else: 
            return self.fields['sum_quantity']

class ProductReceiptItemForm(forms.ModelForm):
    class Meta:
        model = ProductReceiptItem
        fields = ('quantity', 'product_id')
        labels = {
            'quantity': 'Mennyiség',
            'product_id': 'Termék'
        }