from django import forms

from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('status', 'payment_type', 'account_number', 'net_price',
                'gross_price', 'customer_id'
        )
        labels = {
            'status': 'Státusz',
            'payment_type': 'Fizetési mód',
            'account_number': 'Számlaszám',
            'net_price': 'Nettó ár',
            'gross_price': 'Bruttó ár',
            'customer_id': 'Vevő'
        }