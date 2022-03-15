from django.db import models
from django.urls import reverse

import math

from administration.sales_order.models import SalesOrder
from webshop.core.models import CustomUser
from webshop.product.models import PackageType, Product

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'Folyamatban'), # 0-ás indexen kell lennie.
        ('completed', 'Teljesítve'),
        ('cancelled', 'Sztornózva')
    ]
    PAYMENT_TYPE_CHOICES = [
        ('cash', 'Készpénz'),
        ('card', 'Utalás')
    ]
    DELIVERY_MODE_CHOICES = [
        ('personal', 'Személyes átvétel'),
        ('delivery', 'Szállítás'),
    ]
    account_number_key = models.PositiveIntegerField(null=True, blank=True)
    account_number = models.CharField(max_length=20, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    settlement_date = models.DateField(null=True, blank=True)
    net_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    gross_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    debt = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES)
    delivery_mode = models.CharField(max_length=50, choices=DELIVERY_MODE_CHOICES)
    billing_zip_code = models.CharField(max_length=10)
    billing_city = models.CharField(max_length=100)
    billing_street_name = models.CharField(max_length=100)
    billing_house_number = models.CharField(max_length=20)
    deleted = models.BooleanField(default=False)
    conn_sales_order_id = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        if self.account_number is not None:
            return self.account_number
        return f"#{self.id}"

    def get_absolute_url(self):
        return reverse("admin_core:admin_invoice:invoice-detail", kwargs={"id": self.id})

    def get_price(self):
        return math.floor(self.gross_price/100)

    def get_net_price(self):
        return math.floor(self.net_price/100)

    def status_display(self):
        return dict(Invoice.STATUS_CHOICES)[self.status]

    def payment_type_display(self):
        return dict(Invoice.PAYMENT_TYPE_CHOICES)[self.payment_type]

    def is_in_progress(self):
        return self.status == 'in_progress'

class InvoiceItem(models.Model):
    original_name = models.CharField(max_length=100)
    original_producer = models.CharField(max_length=100)
    original_net_price = models.IntegerField(default=0)
    original_vat = models.IntegerField()
    quantity = models.IntegerField()
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    package_type_id = models.ForeignKey(PackageType, on_delete=models.SET_NULL, null=True)
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    def __str__(self):
        if self.invoice_id.account_number is not None:
            if self.product_id is not None:
                return f"{self.invoice_id.account_number} - {self.product_id.name}"
            return f"{self.invoice_id.account_number} - deleted"
        if self.product_id is not None:
            return f"#{self.invoice_id.id} - {self.product_id.name}"
        return f"#{self.invoice_id.id} - deleted"