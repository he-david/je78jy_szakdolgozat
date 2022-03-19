from django.db import models
from django.urls import reverse

import math

from webshop.core.models import CustomUser
from webshop.product.models import PackageType, Product

class DeliveryNote(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'Folyamatban'),
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
    document_number_key = models.PositiveIntegerField(null=True, blank=True)
    document_number = models.CharField(max_length=20, null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    net_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    gross_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES)
    delivery_mode = models.CharField(max_length=50, choices=DELIVERY_MODE_CHOICES)
    shipping_zip_code = models.CharField(max_length=10)
    shipping_city = models.CharField(max_length=100)
    shipping_street_name = models.CharField(max_length=100)
    shipping_house_number = models.CharField(max_length=20)
    deleted = models.BooleanField(default=False)
    conn_sales_order_id = models.ForeignKey('sales_order.SalesOrder', on_delete=models.CASCADE)
    customer_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        if self.document_number is not None:
            return self.document_number
        return f"#{self.id}"

    def get_absolute_url(self):
        return reverse("admin_core:admin_delivery_note:delivery-note-detail", kwargs={"id": self.id})

    def get_price(self):
        return math.floor(self.gross_price/100)

    def get_net_price(self):
        return math.floor(self.net_price/100)

    def status_display(self):
        return dict(DeliveryNote.STATUS_CHOICES)[self.status]

    def delivery_mode_display(self):
        return dict(DeliveryNote.DELIVERY_MODE_CHOICES)[self.delivery_mode]

    def payment_type_display(self):
        return dict(DeliveryNote.PAYMENT_TYPE_CHOICES)[self.payment_type]
    
    def is_in_progress(self):
        return self.status == 'in_progress'

class DeliveryNoteItem(models.Model):
    original_name = models.CharField(max_length=100)
    original_producer = models.CharField(max_length=100)
    original_net_price = models.IntegerField(default=0)
    original_vat = models.IntegerField()
    quantity = models.IntegerField()
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    package_type_id = models.ForeignKey(PackageType, on_delete=models.SET_NULL, null=True)
    delivery_note_id = models.ForeignKey(DeliveryNote, on_delete=models.CASCADE)

    def __str__(self):
        if self.delivery_note_id.document_number is not None:
            return f"{self.delivery_note_id.document_number} - {self.original_name}"
        return f"#{self.delivery_note_id.id} - {self.product_id.name}"