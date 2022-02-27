from django.db import models
from django.contrib.auth.models import AbstractUser

class FAQTopic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    topic_id = models.ForeignKey(FAQTopic, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

    # Own methods
    def is_visible_category(self):
        item = FAQ.objects.filter(topic_id = self.topic_id).values().first()
        return item['id'] == self.id

class CustomUser(AbstractUser):
    pass

class Address(models.Model):
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)
    default = models.BooleanField(default=True)
    customer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.customer_id.username} - address"