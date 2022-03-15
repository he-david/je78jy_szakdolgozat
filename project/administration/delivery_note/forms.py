from django import forms

from .models import DeliveryNote

class DeliveryNoteForm(forms.ModelForm):
    class Meta:
        model = DeliveryNote
        fields = ('status', 'payment_type', 'document_number', 'net_price',
                'gross_price', 'customer_id'
        )