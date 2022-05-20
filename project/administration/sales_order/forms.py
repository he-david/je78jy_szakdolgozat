from django import forms

from .models import SalesOrder

class SalesOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalesOrderForm, self).__init__(*args, **kwargs)
        
        self.fields['status'].widget.attrs['disabled'] = True
        self.fields['payment_type'].widget.attrs['disabled'] = True
        self.fields['document_number'].widget.attrs['readonly'] = True
        self.fields['net_price'].widget.attrs['readonly'] = True
        self.fields['gross_price'].widget.attrs['readonly'] = True
        self.fields['original_customer_name'].widget.attrs['readonly'] = True
        self.fields['order_date'].widget.attrs['readonly'] = True
        self.fields['delivery_mode'].widget.attrs['disabled'] = True
        self.fields['zip_code'].widget.attrs['readonly'] = True
        self.fields['city'].widget.attrs['readonly'] = True
        self.fields['street_name'].widget.attrs['readonly'] = True
        self.fields['house_number'].widget.attrs['readonly'] = True

        self.fields['status'].required = False
        self.fields['payment_type'].required = False
        self.fields['delivery_mode'].required = False
    
    class Meta:
        model = SalesOrder
        fields = ('status', 'payment_type', 'document_number', 'net_price',
                'gross_price', 'original_customer_name', 'order_date',
                'delivery_mode', 'zip_code', 'city', 'street_name', 'house_number'
        )
        labels = {
            'status': 'Státusz',
            'payment_type': 'Fizetési mód',
            'document_number': 'Bizonylatszám',
            'net_price': 'Nettó ár',
            'gross_price': 'Bruttó ár',
            'original_customer_name': 'Vevő',
            'order_date': 'Rendelés dátuma',
            'delivery_mode': 'Szállítási mód',
            'zip_code': 'Irányítószám',
            'city': 'Város',
            'street_name': 'Utca',
            'house_number': 'Házszám'
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

    def clean_document_number(self):
        if self.instance: 
            return self.instance.document_number
        else: 
            return self.fields['document_number']

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

    def clean_order_date(self):
        if self.instance: 
            return self.instance.order_date
        else: 
            return self.fields['order_date']

    def clean_delivery_mode(self):
        if self.instance: 
            return self.instance.delivery_mode
        else: 
            return self.fields['delivery_mode']

    def clean_zip_code(self):
        if self.instance: 
            return self.instance.zip_code
        else: 
            return self.fields['zip_code']
        
    def clean_city(self):
        if self.instance: 
            return self.instance.city
        else: 
            return self.fields['city']
    
    def clean_street_name(self):
        if self.instance: 
            return self.instance.street_name
        else: 
            return self.fields['street_name']

    def clean_house_number(self):
        if self.instance: 
            return self.instance.house_number
        else: 
            return self.fields['house_number']