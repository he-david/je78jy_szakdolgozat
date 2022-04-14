from django import forms

from .models import SalesOrder

class SalesOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalesOrderForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['readonly'] = True
        self.fields['payment_type'].widget.attrs['readonly'] = True
        self.fields['document_number'].widget.attrs['readonly'] = True
        self.fields['net_price'].widget.attrs['readonly'] = True
        self.fields['gross_price'].widget.attrs['readonly'] = True
        self.fields['customer_id'].widget.attrs['readonly'] = True
    
    class Meta:
        model = SalesOrder
        fields = ('status', 'payment_type', 'document_number', 'net_price',
                'gross_price', 'customer_id'
        )
        labels = {
            'status': 'Státusz',
            'payment_type': 'Fizetési mód',
            'document_number': 'Bizonylatszám',
            'net_price': 'Nettó ár',
            'gross_price': 'Bruttó ár',
            'customer_id': 'Vevő'
        }

    def clean_status(self): # Így biztosan nem kaphat más értéket amikor mentésre kerül sor.
        if self.instance: 
            return self.instance.status
        else: 
            return self.fields['status']

    def clean_payment_type(self):
        if self.instance: 
            return self.instance.payment_type
        else: 
            return self.fields['payment_type']

    def clean_document_number(self):
        if self.instance: 
            return self.instance.document_number
        else: 
            return self.fields['document_number']

    def clean_net_price(self):
        if self.instance: 
            return self.instance.net_price*10000
        else: 
            return self.fields['net_price']

    def clean_gross_price(self):
        if self.instance: 
            return self.instance.gross_price*10000
        else: 
            return self.fields['gross_price']
    
    def clean_customer_id(self):
        if self.instance: 
            return self.instance.customer_id
        else: 
            return self.fields['customer_id']