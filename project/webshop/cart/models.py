from django.db import models
from webshop.core.models import CustomUser
from webshop.product.models import PackageType, Product

import math

class Cart(models.Model):
    net_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    gross_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    customer_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer_id.username}'s cart"

    def get_gross_price(self):
        return math.floor(self.gross_price/100)

class CartItem(models.Model):
    quantity = models.IntegerField()
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    package_type_id = models.ForeignKey(PackageType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cart_id} - {self.product_id.name}"

    def get_gross_price(self):
        return math.floor(self.product_id.net_price/100 * (1+self.product_id.vat/100) * 
                            self.package_type_id.quantity * self.quantity)