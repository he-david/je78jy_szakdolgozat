from django import forms

from .models import Invoice

class InvoiceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['disabled'] = True
        self.fields['payment_type'].widget.attrs['disabled'] = True
        self.fields['account_number'].widget.attrs['readonly'] = True
        self.fields['net_price'].widget.attrs['readonly'] = True
        self.fields['gross_price'].widget.attrs['readonly'] = True
        self.fields['original_customer_name'].widget.attrs['readonly'] = True
        self.fields['creation_date'].widget.attrs['readonly'] = True
        self.fields['settlement_date'].widget.attrs['readonly'] = True
        self.fields['delivery_mode'].widget.attrs['disabled'] = True
        self.fields['billing_zip_code'].widget.attrs['readonly'] = True
        self.fields['billing_city'].widget.attrs['readonly'] = True
        self.fields['billing_street_name'].widget.attrs['readonly'] = True
        self.fields['billing_house_number'].widget.attrs['readonly'] = True

        self.fields['status'].required = False
        self.fields['payment_type'].required = False
        self.fields['delivery_mode'].required = False

    class Meta:
        model = Invoice
        fields = ('status', 'payment_type', 'account_number', 'net_price',
                'gross_price', 'original_customer_name', 'creation_date',
                'settlement_date', 'delivery_mode', 'billing_zip_code',
                'billing_city', 'billing_street_name', 'billing_house_number'
        )
        labels = {
            'status': 'Státusz',
            'payment_type': 'Fizetési mód',
            'account_number': 'Számlaszám',
            'net_price': 'Nettó ár',
            'gross_price': 'Bruttó ár',
            'original_customer_name': 'Vevő',
            'creation_date': 'Létrehozás dátuma',
            'settlement_date': 'Kiegyenlítés dátuma',
            'delivery_mode': 'Szállítási mód',
            'billing_zip_code': 'Irányítószám',
            'billing_city': 'Város',
            'billing_street_name': 'Utca',
            'billing_house_number': 'Házszám',
        }
    
    def clean_status(self): # Így biztosan nem kaphat más értéket amikor mentésre kerül sor.
        if self.instance: 
            return self.instance.status
        else: 
            return self.fields['status']

    def clean_payment_type(self):
        if self.instance: 
            return self.instance.payment_type
        else: 
            return self.fields['payment_type']

    def clean_account_number(self):
        if self.instance: 
            return self.instance.account_number
        else: 
            return self.fields['account_number']

    def clean_net_price(self):
        if self.instance: 
            return self.instance.net_price*10000
        else: 
            return self.fields['net_price']

    def clean_gross_price(self):
        if self.instance: 
            return self.instance.gross_price*10000
        else: 
            return self.fields['gross_price']
    
    def clean_original_customer_name(self):
        if self.instance: 
            return self.instance.original_customer_name
        else: 
            return self.fields['original_customer_name']
        
    def clean_creation_date(self):
        if self.instance: 
            return self.instance.creation_date
        else: 
            return self.fields['creation_date']

    def clean_settlement_date(self):
        if self.instance: 
            return self.instance.settlement_date
        else: 
            return self.fields['settlement_date']

    def clean_delivery_mode(self):
        if self.instance: 
            return self.instance.delivery_mode
        else: 
            return self.fields['delivery_mode']

    def clean_billing_zip_code(self):
        if self.instance: 
            return self.instance.billing_zip_code
        else: 
            return self.fields['billing_zip_code']

    def clean_billing_city(self):
        if self.instance: 
            return self.instance.billing_city
        else: 
            return self.fields['billing_city']

    def clean_billing_street_name(self):
        if self.instance: 
            return self.instance.billing_street_name
        else: 
            return self.fields['billing_street_name']

    def clean_billing_house_number(self):
        if self.instance: 
            return self.instance.billing_house_number
        else: 
            return self.fields['billing_house_number']