from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser, Address

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_staff', 'first_name', 'last_name', 'groups')

class AddressChangeForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('zip_code', 'city', 'street_name', 'house_number')
        labels = {
            'zip_code': 'Irányítószám',
            'city': 'Város',
            'street_name': 'Utca',
            'house_number': 'Házszám'
        }