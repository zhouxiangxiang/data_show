
from django.conf.urls import url

#from .views import graph, play_count_by_month, show
from .views import *

urlpatterns = [
    url(r'^$', get_index),
    url(r'^index', get_index),
    url(r'^index.html', get_index),
    url(r'^show_data', get_data),
    url(r'^show', show),
    url(r'^data.tsv', data_tsv),
    url(r'^api/play_count_by_month', play_count_by_month, name='paly_count'),
    url(r'^templates/.*.css', data_css),
]
