from django.db import models
from django.urls import reverse

class ProductReceipt(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'Folyamatban'),
        ('final', 'Végleges')
    ]
    document_number_key = models.PositiveIntegerField(null=True, blank=True)
    document_number = models.CharField(max_length=20, null=True, blank=True)
    finalization_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    sum_quantity = models.IntegerField(default=0)

    def __str__(self):
        if self.document_number is not None:
            return self.document_number
        return f"#{self.id}"

    def get_absolute_url(self):
        return reverse("admin_core:admin_product_receipt:product-receipt-detail", kwargs={"id": self.id})

    def is_in_progress(self):
        return self.status == 'in_progress'
    
class ProductReceiptItem(models.Model):
    original_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    product_id = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True)
    product_receipt_id = models.ForeignKey(ProductReceipt, on_delete=models.CASCADE)