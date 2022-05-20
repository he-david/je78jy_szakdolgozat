from django.db import models

class SalesBase(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('cash', 'Készpénz'),
        ('card', 'Utalás')
    ]
    DELIVERY_MODE_CHOICES = [
        ('personal', 'Személyes átvétel'),
        ('delivery', 'Szállítás'),
    ]
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES)
    delivery_mode = models.CharField(max_length=50, choices=DELIVERY_MODE_CHOICES)
    net_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    gross_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)
    deleted = models.BooleanField(default=False)
    original_customer_name = models.CharField(max_length=100)
    customer_id = models.ForeignKey('core.CustomUser', on_delete=models.SET_NULL, null=True)

class SalesItemBase(models.Model):
    original_name = models.CharField(max_length=100)
    original_producer = models.CharField(max_length=100)
    original_net_price = models.IntegerField(default=0)
    original_vat = models.IntegerField()
    original_package_quantity = models.PositiveIntegerField()
    original_package_display = models.CharField(max_length=50)
    quantity = models.IntegerField()
    product_id = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True)
    package_type_id = models.ForeignKey('product.PackageType', on_delete=models.SET_NULL, null=True)