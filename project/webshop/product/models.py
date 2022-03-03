from django.db import models
from django.urls import reverse

import math

class Action(models.Model):
    name = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return self.name

class PackageType(models.Model):
    summary_name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.display_name

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    net_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    vat = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    free_stock = models.IntegerField(default=0)
    reserved_stock = models.IntegerField(default=0)
    image = models.ImageField(blank=True, null=True, upload_to='product_images')
    slug = models.SlugField(unique=True)
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    package_type_id = models.ManyToManyField(PackageType)
    action_id = models.ManyToManyField(Action, blank=True)

    def __str__(self):
        return self.name

    # Own methods
    def get_absolute_url(self):
        return reverse('webshop_product:product-detail', kwargs={'slug': self.slug})

    def get_price(self):
        return math.floor(self.net_price/100 * (1+self.vat/100))

    
    