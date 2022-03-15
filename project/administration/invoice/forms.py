from django import forms

from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('status', 'payment_type', 'account_number', 'net_price',
                'gross_price', 'customer_id'
        )