from __future__ import unicode_literals

from django.db import models

from .fetch_data import *

# Create your models here.

class Play(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()


class  SpeedData:
    def __init__(self):
        self.db_info = DataBaseInfo('10.0.6.27', '3306', 'root', '123', 'DYN_PARENTS')
        self.fd = FetchSpeedData(self.db_info)
        self.tb_name = 'tmp'

    def get_node_name(self, nr):  # node room
        nn = self.fd.get_node_name(self.tb_name, nr)
        return nn

    def get_node_name_data(self, nn): # node name
        data = self.fd.get_node_name_data(self.tb_name, nn)
        return data

    def get_node_name_speed_time(self, nn):
        data =  self.fd.get_nn_ST(self.tb_name, nn) # speed time
        return data
