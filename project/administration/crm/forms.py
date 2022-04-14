from django import forms

from webshop.core.models import FAQ, Contact, FAQTopic

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['readonly'] = True
        self.fields['last_name'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['message'].widget.attrs['readonly'] = True
    
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'message')
        labels = {
            'first_name': 'Keresztnév',
            'last_name': 'Vezetéknév',
            'email': 'E-mail',
            'message': 'Üzenet',
        }

    def clean_first_name(self): # Így biztosan nem kaphat más értéket amikor mentésre kerül sor.
        if self.instance: 
            return self.instance.first_name
        else: 
            return self.fields['first_name']

    def clean_last_name(self):
        if self.instance: 
            return self.instance.last_name
        else: 
            return self.fields['last_name']

    def clean_email(self):
        if self.instance: 
            return self.instance.email
        else: 
            return self.fields['email']

    def clean_message(self):
        if self.instance: 
            return self.instance.message
        else: 
            return self.fields['message']

class FaqTopicForm(forms.ModelForm):
    class Meta:
        model = FAQTopic
        fields = ('name',)
        labels = {'name': 'Témakör'}

class FaqForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ('question', 'answer', 'topic_id')
        labels = {
            'question': 'Kérdés',
            'answer': 'Válasz',
            'topic_id': 'Témakör',
        }