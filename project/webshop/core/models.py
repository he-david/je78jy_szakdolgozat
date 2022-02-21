from django.db import models

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