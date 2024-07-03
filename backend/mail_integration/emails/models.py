from django.db import models

# Create your models here.
class EmailAccount(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class EmailMessage(models.Model):
    email = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    date_sent = models.DateTimeField()
    date_recieved = models.DateTimeField()
    body = models.TextField()
    attachments = models.JSONField()

    def __str__(self):
        return self.topic