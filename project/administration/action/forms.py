from django import forms

from webshop.product.models import Action

class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ('name', 'percent', 'from_date', 'to_date')
        labels = {
            'name': 'Megnevezés',
            'percent': 'Százalék',
            'from_date': 'Kezdet',
            'to_date': 'Vég',
        }
        widgets = {
            'from_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type':'date'}),
            'to_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type':'date'}),
        }