from django.shortcuts import render

# Create your views here.

from django.db import connections
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse

from .models import Play

def graph(request):
    #return HttpResponse("hello world. You are at the d3 index")
    #return render(request, 'data_show/graph.html')
    return render(request, 'data_show/index.html')

def show(request):
    return render(request, 'data_show/show.html')

def data_tsv(request):
    fd = open('./data_show/data/data.tsv', 'r')
    data = HttpResponse(fd.read())
    fd.close()

    return data

def data_css(request):
    fd = open('./data_show/templates/data_show/css/style.css', 'r')
    data = HttpResponse(fd.read())
    fd.close()

    return data

def play_count_by_month(request):
    #data = Play.objects.all() \
    #        .extra(select={'month': connections[Play.objects.db].ops.date_trunc_sql('moth', 'date')}) \
    #        .values('month') \
    #        .annotate(count_items=Count('id'))
    #
    #return JsonResponser(list(data), safe=False)
    return HttpResponse("hello world. You are at the d3 index")







