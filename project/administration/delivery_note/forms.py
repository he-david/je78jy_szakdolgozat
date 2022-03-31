from django import forms

from .models import DeliveryNote

class DeliveryNoteForm(forms.ModelForm):
    class Meta:
        model = DeliveryNote
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