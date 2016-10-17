from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Play(models.Model):
    name = model.CharField(max_length=100)
    date = model.DateTimeField()

