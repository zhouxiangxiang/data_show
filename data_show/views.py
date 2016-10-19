from django.shortcuts import render

# Create your views here.
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
            return HttpResponse(form.cleaned_data['node_room'])
        else:
            form = NameForm()
            return render(request, 'data_show/index.html', {'form': form})

    sd = SpeedData()
    raw_nr = sd.get_node_room()

    node_room = { "CUN": [], "CTN": [], "CMN": [], "OTH":[] }
    for item in raw_nr:
        if item.startswith("CUN"):
            node_room["CUN"].append(item)
        elif item.startswith("CTN"):
            node_room["CTN"].append(item)
        elif item.startswith("CMN"):
            node_room["CMN"].append(item)
        else:
            node_room["OTH"].append(item)

    json_str = json.dumps({'node_room': node_room})
    return render(request, 'data_show/index.html', {'data': json_str})

def get_data(request):
    if request.method == 'POST':
        form = NodeForm(request.POST)
        if form.is_valid():
            node_room = form.cleaned_data['node_room']

            sd = SpeedData()
            node_name = sd.get_node_name(node_room)

            print(node_room)
            print(node_name)

            data = []
            for item in node_name:
                data_nn = sd.get_node_name_speed_time(item, "220.181.77.98")
                # sort by timestamp
                def getKey(tmp):
                    return tmp[1];
                data_nn = sorted(data_nn, key=getKey)

                start = 0
                for i in range(len(data_nn)):
                    s_t = data_nn[i]
                    if not start:
                        start = s_t[1]
                    else:
                        st_tm = datetime.datetime.fromtimestamp(start).strftime('%Y-%m-%d')
                        cur_tm = datetime.datetime.fromtimestamp(s_t[1]).strftime('%Y-%m-%d')
                        if st_tm != cur_tm:
                            break;

                    s_t = [s_t[0] / 1024,
                           datetime.datetime.fromtimestamp(s_t[1]).strftime('%Y-%m-%d %H:%M:%S')]
                    data_nn[i] = s_t 

                data.append({'node_name': item, 'data': data_nn})

            json_str = json.dumps(data)
            print(json_str)

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
