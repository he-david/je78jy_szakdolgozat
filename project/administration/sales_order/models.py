from django.db import models
from django.urls import reverse

import math

from webshop.core.models import CustomUser, Address
from webshop.product.models import PackageType, Product

class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'Folyamatban'),
        ('partially_completed', 'Részben teljesítve'),
        ('completed', 'Teljesített'),
        ('cancelled', 'Lemondva')
    ]
    PAYMENT_TYPE_CHOICES = [
        ('cash', 'Készpénz'),
        ('card', 'Utalás')
    ]
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES)
    document_number_key = models.PositiveIntegerField(null=True, blank=True)
    document_number = models.CharField(max_length=20, null=True, blank=True) # VME-2022/1, mert véglegesítéskor generálódik
    net_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    gross_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    deleted = models.BooleanField(default=False)
    shipping_address_id = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    customer_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        if self.document_number is not None:
            return self.document_number
        return f"#{self.id}"

    def get_absolute_url(self):
        return reverse("admin_core:admin_sales_order:sales-order-detail", kwargs={"id": self.id})

    def get_price(self):
        return math.floor(self.gross_price/100)

    def get_net_price(self):
        return math.floor(self.net_price/100)

    def status_display(self):
        return dict(SalesOrder.STATUS_CHOICES)[self.status]

    def payment_type_display(self):
        return dict(SalesOrder.PAYMENT_TYPE_CHOICES)[self.payment_type]

    def is_in_progress(self):
        return self.status == 'in_progress'

class SalesOrderItem(models.Model):
    original_name = models.CharField(max_length=100)
    original_producer = models.CharField(max_length=100)
    original_net_price = models.IntegerField(default=0)
    original_vat = models.IntegerField()
    quantity = models.IntegerField()
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    package_type_id = models.ForeignKey(PackageType, on_delete=models.SET_NULL, null=True)
    sales_order_id = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)

    def __str__(self):
        if self.sales_order_id.document_number is not None:
            if self.product_id is not None:
                return f"{self.sales_order_id.document_number} - {self.product_id.name}"
            return f"{self.sales_order_id.document_number} - deleted"
        if self.product_id is not None:
            return f"#{self.sales_order_id.id} - {self.product_id.name}"
        return f"#{self.sales_order_id.id} - deleted"