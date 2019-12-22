from django.db import models
from django.utils import timezone


class Item(models.Model):
    text = models.TextField(default='')
    creation_time = models.DateTimeField(default=timezone.now)
