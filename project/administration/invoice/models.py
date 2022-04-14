from django.db import models
from django.urls import reverse

import math

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'Folyamatban'), # 0-ás indexen kell lennie.
        ('completed', 'Kiegyenlítve'),
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
    debt = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$ # Bruttóban van.
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES)
    delivery_mode = models.CharField(max_length=50, choices=DELIVERY_MODE_CHOICES)
    billing_zip_code = models.CharField(max_length=10)
    billing_city = models.CharField(max_length=100)
    billing_street_name = models.CharField(max_length=100)
    billing_house_number = models.CharField(max_length=20)
    deleted = models.BooleanField(default=False)
    conn_sales_order_id = models.ForeignKey('sales_order.SalesOrder', on_delete=models.CASCADE)
    customer_id = models.ForeignKey('core.CustomUser', on_delete=models.SET_NULL, null=True) # Nincs vele gond, mert customert nem lehet törölni.

    def __str__(self):
        if self.account_number is not None:
            return self.account_number
        return f"#{self.id}"

    def get_absolute_url(self):
        return reverse("admin_core:admin_invoice:invoice-detail", kwargs={"id": self.id})

    def get_gross_price(self):
        return math.floor(self.gross_price/100)

    def get_net_price(self):
        return math.floor(self.net_price/100)

    def is_in_progress(self):
        return self.status == 'in_progress'

class InvoiceItem(models.Model):
    original_name = models.CharField(max_length=100)
    original_producer = models.CharField(max_length=100)
    original_net_price = models.IntegerField(default=0)
    original_vat = models.IntegerField()
    original_package_quantity = models.PositiveIntegerField() # Mert törölhetik a package_typeot
    original_package_display = models.CharField(max_length=50)
    quantity = models.IntegerField()
    product_id = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True)
    package_type_id = models.ForeignKey('product.PackageType', on_delete=models.SET_NULL, null=True)
    invoice_id = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        if self.invoice_id.account_number is not None:
            if self.product_id is not None:
                return f"{self.invoice_id.account_number} - {self.product_id.name}"
            return f"{self.invoice_id.account_number} - deleted"
        if self.product_id is not None:
            return f"#{self.invoice_id.id} - {self.product_id.name}"
        return f"#{self.invoice_id.id} - deleted"

    def get_original_net_price(self):
        return math.floor(self.original_net_price/100 * self.original_package_quantity * self.quantity)

    def get_original_gross_price(self):
        return math.floor(self.original_net_price/100 * (1 + self.original_vat/100) * self.original_package_quantity * self.quantity)