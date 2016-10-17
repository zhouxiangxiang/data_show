from django.shortcuts import render

# Create your views here.

from django.db import connections
from django.db.models import Count
from django.http import JsonResponser 
from django.shortcuts import render

from .models import Play

def graph(request):
    return render(request, 'graph/graph.html')

def play_count_by_month(request):
    data = Play.objects.all() \
            .extra(select={'month': connections[Play.objects.db].ops.date_trunc_sql('moth', 'date')}) \
            .values('month') \
            .annotate(count_items=Count('id'))
    
    return JsonResponser(list(data), safe=False)






