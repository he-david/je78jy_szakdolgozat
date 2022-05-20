from django.db import models
from django.urls import reverse
from django.utils import timezone

import math

from administration.delivery_note.models import DeliveryNote
from administration.invoice.models import Invoice
from administration.admin_core.models import SalesBase, SalesItemBase

class SalesOrder(SalesBase):
    STATUS_CHOICES = [
        ('in_progress', 'Folyamatban'),
        ('partially_completed', 'Részben teljesítve'),
        ('completed', 'Teljesítve'),
        ('cancelled', 'Lemondva')
    ]
    order_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    document_number_key = models.PositiveIntegerField(null=True, blank=True)
    document_number = models.CharField(max_length=20, null=True, blank=True)
    
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

    def get_status_percent(self):
        if self.status == 'in_progress':
            return 0
        elif self.status == 'partially_completed':
            return 50
        elif self.status == 'completed':
            return 100
        else:
            return -1

    def is_in_progress(self):
        return self.status == 'in_progress'

    def is_partially_completed(self):
        return self.status == 'partially_completed'

    def has_invoice(self):
        return Invoice.objects.filter(conn_sales_order_id=self.id, deleted=False).exists()
    
    def has_view_invoice(self):
        return (Invoice.objects.filter(conn_sales_order_id=self.id, deleted=False).exists() or
                self.status == 'cancelled')

    def has_delivery_note(self):
        return DeliveryNote.objects.filter(conn_sales_order_id=self.id, deleted=False).exists()

    def has_view_delivery_note(self):
        return (DeliveryNote.objects.filter(conn_sales_order_id=self.id, deleted=False).exists() or
                self.delivery_mode == 'personal' or self.status == 'cancelled')

class SalesOrderItem(SalesItemBase):
    sales_order_id = models.ForeignKey(SalesOrder, related_name='items' , on_delete=models.CASCADE)

    def __str__(self):
        if self.sales_order_id.document_number is not None:
            return f"{self.sales_order_id.document_number} - {self.original_name}"
        return f"#{self.sales_order_id.id} - {self.original_name}"

    def get_original_net_price(self):
        return math.floor(self.original_net_price/100 * self.original_package_quantity * self.quantity)

    def get_original_gross_price(self):
        return math.floor(self.original_net_price/100 * (1 + self.original_vat/100) * self.original_package_quantity * self.quantity)