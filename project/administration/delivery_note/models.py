from django.db import models
from django.urls import reverse

import math

from administration.admin_core.models import SalesBase, SalesItemBase

class DeliveryNote(SalesBase):
    STATUS_CHOICES = [
        ('in_progress', 'Folyamatban'),
        ('completed', 'Teljesítve'),
        ('cancelled', 'Lemondva')
    ]
    document_number_key = models.PositiveIntegerField(null=True, blank=True)
    document_number = models.CharField(max_length=20, null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    conn_sales_order_id = models.ForeignKey('sales_order.SalesOrder', on_delete=models.CASCADE)

    def __str__(self):
        if self.document_number is not None:
            return self.document_number
        return f"#{self.id}"

    def get_absolute_url(self):
        return reverse("admin_core:admin_delivery_note:delivery-note-detail", kwargs={"id": self.id})

    def get_gross_price(self):
        return math.floor(self.gross_price/100)

    def get_net_price(self):
        return math.floor(self.net_price/100)
    
    def is_in_progress(self):
        return self.status == 'in_progress'

class DeliveryNoteItem(SalesItemBase):
    delivery_note_id = models.ForeignKey(DeliveryNote, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        if self.delivery_note_id.document_number is not None:
            return f"{self.delivery_note_id.document_number} - {self.original_name}"
        return f"#{self.delivery_note_id.id} - {self.product_id.name}"

    def get_original_net_price(self):
        return math.floor(self.original_net_price/100 * self.original_package_quantity * self.quantity)

    def get_original_gross_price(self):
        return math.floor(self.original_net_price/100 * (1 + self.original_vat/100) * self.original_package_quantity * self.quantity)