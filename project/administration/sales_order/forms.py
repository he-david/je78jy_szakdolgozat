from django import forms

from .models import SalesOrder

class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ('status', 'payment_type', 'document_number', 'net_price',
                'gross_price', 'shipping_address_id', 'customer_id'
        )