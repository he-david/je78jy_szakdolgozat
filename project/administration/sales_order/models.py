from django.db import models

from webshop.core.models import CustomUser, Address
from webshop.product.models import PackageType, Product

class SalesOrder(models.Model):
    recording_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=(
        ('ordered', 'Megrendelve'),
        ('billed', 'Számlázva'),
        ('on_delivery_note', 'Szállítólevélen')
    ))
    payment_type = models.CharField(max_length=20, choices=(
        ('cash', 'Készpénz'),
        ('card', 'Utalás'),
    ))
    document_number_key = models.PositiveIntegerField(null=True, blank=True)
    document_number = models.CharField(max_length=20, null=True, blank=True) # VME-2022/1, mert véglegesítéskor generálódik
    final = models.BooleanField(default=False)
    net_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    gross_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    deleted = models.BooleanField(default=False)
    shipping_address_id = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    customer_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        if self.document_number is not None:
            return self.document_number
        return f"#{self.id}"

class SalesOrderItem(models.Model):
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