
from django.conf.urls import url

#from .views import graph, play_count_by_month, show
from .views import *

urlpatterns = [
    url(r'^$', get_index),
    url(r'^index', get_index),
    url(r'^index.html', get_index),
    url(r'^show_data', get_data),
    url(r'^show', show),
    url(r'^templates/.*.css', data_css),
    # --
    url(r'^test', test_chart),
    url(r'^test_data.csv', test_data_csv),
    url(r'^line_chart', line_chart),
    url(r'^data.csv', data_csv),
]
