from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from .models import Contact, CustomUser, Address

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].label = 'Felhasználónév'
        self.fields['password1'].label = 'Jelszó'
        self.fields['password2'].label = 'Jelszó megerősítés'

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        labels = {
            'username': 'Felhasználónév',
            'email': 'E-mail',
        }

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.error_messages = {
            'invalid_login': "Kérem adjon meg egy helyes felhasználónevet és jelszót.",
            'inactive': "A felhasználó inaktív.",
        }
        self.fields['username'].label = 'Felhasználónév'
        self.fields['password'].label = 'Jelszó'

        for fieldname in ['username', 'password']:
            self.fields[fieldname].help_text = None

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

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name' , 'last_name', 'email', 'message')
        labels = {
            'last_name': 'Vezetéknév',
            'first_name': 'Keresztnév',
            'email': 'E-mail',
            'message': 'Üzenet'
        }