from django.db import models
from django.urls import reverse

import math

from administration.delivery_note.models import DeliveryNote # TODO HEDA oda vissza van import :c
from administration.invoice.models import Invoice
from webshop.core.models import CustomUser
from webshop.product.models import PackageType, Product

class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'Folyamatban'),
        ('partially_completed', 'Részben teljesítve'),
        ('completed', 'Teljesítve'),
        ('cancelled', 'Lemondva')
    ]
    PAYMENT_TYPE_CHOICES = [
        ('cash', 'Készpénz'),
        ('card', 'Utalás')
    ]
    DELIVERY_MODE_CHOICES = [
        ('personal', 'Személyes átvétel'),
        ('delivery', 'Szállítás'),
    ]
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES)
    delivery_mode = models.CharField(max_length=50, choices=DELIVERY_MODE_CHOICES)
    document_number_key = models.PositiveIntegerField(null=True, blank=True)
    document_number = models.CharField(max_length=20, null=True, blank=True) # VME-2022/1, mert véglegesítéskor generálódik
    net_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    gross_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)
    deleted = models.BooleanField(default=False)
    customer_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        app_label = 'sales_order'

    def __str__(self):
        if self.document_number is not None:
            return self.document_number
        return f"#{self.id}"


    def get_absolute_url(self):
        return reverse("admin_core:admin_sales_order:sales-order-detail", kwargs={"id": self.id})

    def get_gross_price(self):
        return math.floor(self.gross_price/100)

    def get_net_price(self):
        return math.floor(self.net_price/100)

    def status_display(self):
        return dict(SalesOrder.STATUS_CHOICES)[self.status]

    def payment_type_display(self):
        return dict(SalesOrder.PAYMENT_TYPE_CHOICES)[self.payment_type]

    def has_invoice(self):
        return Invoice.objects.filter(conn_sales_order_id=self.id).exists()

    def has_delivery_note(self):
        return (DeliveryNote.objects.filter(conn_sales_order_id=self.id).exists() or
                self.delivery_mode == 'personal')

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
            return f"{self.sales_order_id.document_number} - {self.original_name}"
        return f"#{self.sales_order_id.id} - {self.original_name}"