from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

import math

from administration.invoice.models import Invoice

class FAQTopic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("admin_core:crm:faq-topic-detail", kwargs={"id": self.id})

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    topic_id = models.ForeignKey(FAQTopic, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse("admin_core:crm:faq-detail", kwargs={"id": self.id})

    def is_visible_category(self):
        item = FAQ.objects.filter(topic_id = self.topic_id).values().first()
        return item['id'] == self.id

class CustomUser(AbstractUser):
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    def get_spent_net_money(self):
        return math.floor((sum(Invoice.objects.filter(customer_id=self.id, debt=0, deleted=False).values_list('net_price', flat=True)))/100)

    def get_spent_gross_money(self):
        return math.floor((sum(Invoice.objects.filter(customer_id=self.id, debt=0, deleted=False).values_list('gross_price', flat=True)))/100)

    def get_debt(self):
        return math.floor((sum(Invoice.objects.filter(~Q(debt=0), customer_id=self.id, deleted=False).values_list('debt', flat=True)))/100)

class Address(models.Model):
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)
    customer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.customer_id.username} - address"

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.email}"

    def get_absolute_url(self):
        return reverse("admin_core:crm:message-detail", kwargs={"id": self.id})