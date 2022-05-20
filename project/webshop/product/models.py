from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.core.validators import MaxValueValidator

import math
from datetime import date

from administration.admin_product import utils as admin_product_utils

class Action(models.Model):
    name = models.CharField(max_length=100)
    percent = models.PositiveIntegerField(validators=[MaxValueValidator(100)], error_messages={'max_value': 'Az érték legyen kisebb van egyenlő, mint 100.'})
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('admin_core:admin_action:action-detail', kwargs={'id': self.id})

class PackageType(models.Model):
    summary_name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.summary_name

    def get_absolute_admin_url(self):
        return reverse('admin_core:admin_product:package-detail', kwargs={'id': self.id})
    
    def is_deletable(self):
        return Product.objects.filter(package_type_id=self.id).count() == 0

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_id = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

    def get_absolute_admin_url(self):
        return reverse('admin_core:admin_category:category-detail', kwargs={'id': self.id})

    def get_product_count(self):
        return Product.objects.filter(category_id=self.id).count()

class Product(models.Model):
    name = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    net_price = models.IntegerField(default=0) # 1000 -> 10Ft, 1000 -> 10.00$
    vat = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    free_stock = models.IntegerField(default=0)
    reserved_stock = models.IntegerField(default=0)
    image = models.ImageField(blank=True, null=True, upload_to='product_images/')
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_id = models.ForeignKey(Category, related_name='items', on_delete=models.SET_NULL, blank=True, null=True)
    package_type_id = models.ManyToManyField(PackageType)
    action_id = models.ManyToManyField(Action, blank=True)

    class Meta:
        app_label='product'

    def __str__(self):
        return self.name    

    def get_absolute_url(self):
        return reverse('webshop_product:product-detail', kwargs={'slug': self.slug})

    def get_absolute_admin_url(self):
        return reverse('admin_core:admin_product:product-detail', kwargs={'id': self.id})

    def get_action_percent(self):
        today = date.today()
        percent = 0

        for action in self.action_id.all():
            if (action.from_date <= today and today <= action.to_date) and percent < action.percent:
                percent = action.percent
        return percent

    def get_net_price(self):
        return math.floor(self.net_price * (1 - self.get_action_percent() / 100))

    def get_admin_view_net_price(self):
        return math.floor(self.net_price/100)
    
    def get_admin_view_gross_price(self):
        return math.floor(self.net_price/100 * (1 + self.vat / 100))

    def get_view_net_price(self):
        return math.floor(self.net_price/100 * (1 - self.get_action_percent() / 100))

    def get_view_gross_price(self):
        return math.floor(self.net_price/100 * (1 - self.get_action_percent() / 100) * (1 + self.vat / 100))
    
    def get_positive_stock_movement_sum(self):
        return admin_product_utils.get_positive_stock_movement_sum(self)

    def get_negative_stock_movement_sum(self):
        return admin_product_utils.get_negative_stock_movement_sum(self)

    def has_no_open_document(self):
        return admin_product_utils.has_no_open_document(self)

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        new_slug = slugify(instance.name)

        if Product.objects.filter(slug=new_slug).exists():
            instance.slug = f"{new_slug}_{instance.id}"
        else:
            instance.slug = new_slug
        instance.save()

post_save.connect(slug_generator, sender=Product)