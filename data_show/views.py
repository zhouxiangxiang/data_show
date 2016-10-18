from django.shortcuts import render

# Create your views here.
#from datetime import datetime
import datetime
import json

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
            node_name = form.cleaned_data['node_name']

            sd = SpeedData()
            nn = sd.get_node_name(node_name)
            data = []
            for item in nn:
                data_nn = sd.get_node_name_speed_time(item)
                for i in range(len(data_nn)):
                    s_t = data_nn[i]
                    s_t = [s_t[0],
                            str(datetime.datetime.fromtimestamp(int(s_t[1])).strftime('%Y-%m-%d %H:%M:%S'))]
                           #datetime.datetime.fromtimestamp(int(s_t[1])).strftime('%H:%M:%S'))
                    data_nn[i] = s_t 
                for s_t in data_nn:
                    print(s_t)
                data.append(data_nn)

                pass_data = {'node_name': nn, 'data': data[0]}
                json_str = json.dumps(pass_data)

            #return render(request, 'data_show/show_data.html', {'node_name': nn, 'data': data[0]})
            return render(request, 'data_show/show_data.html', {"data": json_str})
        else:
            form = NodeForm()
            return render(request, 'data_show/index.html', {'form': form})

    return render(request, 'data_show/index.html')

def line_chart(request):
    return render(request, 'data_show/line_chart.html')

def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponse('thanks')
        else:
            form = NameForm()

        return render(request, 'data_show/index', {'form': form})

def show(request):
    sd = SpeedData()
    data = sd.get_data()
    template = loader.get_template('data_show/show.html')
    context = {
            'data_show': data,
            'title': 'title',
    }
    return HttpResponse(template.render(context, request))

def data_css(request):
    fd = open('./data_show/templates/data_show/css/style.css', 'r')
    data = HttpResponse(fd.read())
    fd.close()

    return data

def data_csv(request):
    fd = open('./data_show/templates/data_show/data.csv', 'r')
    data = HttpResponse(fd.read())
    fd.close()

    return data
