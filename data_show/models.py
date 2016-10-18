from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Play(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()


class  SpeedData:
    def __init__(self):
        pass

    def get_data(self):
        data = [1, 2, 3, 4, 5]
        return data

