from django import forms

from administration.sales_order.models import SalesOrder
from webshop.core.models import CustomUser

class PaymentPersonalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentPersonalForm, self).__init__(*args, **kwargs)
        
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True

    class Meta:
        model = CustomUser
        fields = ('last_name', 'first_name')
        labels = {
            'last_name': 'Vezetéknév',
            'first_name': 'Keresztnév'
        }

class PaymentOrderDataForm(forms.Form):
    payment_type = forms.ChoiceField(choices=SalesOrder.PAYMENT_TYPE_CHOICES, label='Fizetési mód')
    delivery_mode = forms.ChoiceField(choices=SalesOrder.DELIVERY_MODE_CHOICES, label='Szállítási mód')