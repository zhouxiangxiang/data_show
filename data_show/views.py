from django.shortcuts import render

# Create your views here.

from django.db import connections
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import *

from .forms import *

def get_index(request):
    if request.method == 'POST':
        form = NodeForm(request.POST)
        if form.is_valid():
            return HttpResponse(form.cleaned_data['node_name'])
        else:
            form = NameForm()
            return render(request, 'data_show/index.html', {'form': form})

    return render(request, 'data_show/index.html')

def get_data(request):
    if request.method == 'POST':
        form = NodeForm(request.POST)
        if form.is_valid():
            #return HttpResponse(form.cleaned_data['node_name'])
            return HttpResponse(form.cleaned_data['node_name'])
        else:
            form = NodeForm()
            return render(request, 'data_show/index.html', {'form': form})

    return render(request, 'data_show/index.html')

def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponse('thanks')
        else:
            form = NameForm()

        return render(request, 'data_show/index', {'form': form})

#def graph(request):
    #return HttpResponse("hello world. You are at the d3 index")
    #return render(request, 'data_show/graph.html')
#    return render(request, 'index')

def show(request):
    # return render(request, 'data_show/show.html')

    # read data from database
    sd = SpeedData()
    data = sd.get_data()
    template = loader.get_template('data_show/show.html')
    context = {
            'data_show': data,
            'title': 'title',
    }
    return HttpResponse(template.render(context, request))

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

