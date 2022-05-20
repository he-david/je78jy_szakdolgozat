from django.db import models
from django.urls import reverse
from django.utils import timezone

import math

from administration.admin_core.models import SalesBase, SalesItemBase

class Invoice(SalesBase):
    STATUS_CHOICES = [
        ('in_progress', 'Folyamatban'),
        ('completed', 'Kiegyenlítve'),
        ('cancelled', 'Sztornózva')
    ]
    account_number_key = models.PositiveIntegerField(null=True, blank=True)
    account_number = models.CharField(max_length=20, null=True, blank=True)
    creation_date = models.DateField(default=timezone.now)
    settlement_date = models.DateField(null=True, blank=True)
    debt = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$ - Bruttóban van.
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    conn_sales_order_id = models.ForeignKey('sales_order.SalesOrder', on_delete=models.CASCADE)

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

class InvoiceItem(SalesItemBase):
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