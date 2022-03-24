from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.utils.text import slugify

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

    def get_absolute_admin_url(self):
        return reverse('admin_core:admin_product:package-detail', kwargs={'id': self.id})
    
    def is_deletable(self):
        if Product.objects.filter(package_type_id=self.id).count() == 0:
            return True
        else:
            return False

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_id = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return f"{self.id} - {self.name}"

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
    image = models.ImageField(blank=True, null=True, upload_to='product_images')
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    package_type_id = models.ManyToManyField(PackageType)
    action_id = models.ManyToManyField(Action, blank=True)

    def __str__(self):
        return self.name    

    def get_absolute_url(self):
        return reverse('webshop_product:product-detail', kwargs={'slug': self.slug})

    def get_absolute_admin_url(self):
        return reverse('admin_core:admin_product:product-detail', kwargs={'id': self.id})

    def get_price(self):
        return math.floor(self.net_price/100 * (1+self.vat/100))

    
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        new_slug = slugify(instance.name)

        if Product.objects.filter(slug=new_slug).exists():
            instance.slug = f"{new_slug}_{instance.id}"
        else:
            instance.slug = new_slug
        instance.save()

post_save.connect(slug_generator, sender=Product)