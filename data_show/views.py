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
            t_node = sd.get_transfer_node()


            # all the data for a node room(which has many node names(machines))
            data = []
            for i_nn in node_name:

                # all the data for a node name(which has many transfer nodes)
                tn_data = []
                for i_tn in t_node:
                    data_nn = sd.get_node_name_speed_time(i_nn, i_tn)
                    if not data_nn:
                        continue

                    # sort by timestamp
                    def getKey(tmp):
                        return tmp[1];
                    data_nn = sorted(data_nn, key=getKey)

                    secs_day = 86400 # 24 * 60 * 60
                    start_tm = data_nn[0][1]
                    for i in range(len(data_nn)):
                        s_t = data_nn[i]

                        if s_t[1]  - start_tm >= secs_day:
                            data_nn = data_nn[:i]
                            break

                        data_nn[i] = [s_t[0] / 1024,
                                      datetime.datetime.fromtimestamp(s_t[1]).strftime('%Y-%m-%d %H:%M:%S')]


                    tn_data.append({'t_node':t_node, 'data' : data_nn })
                data.append( {'node_name': i_nn, 'tn_data': tn_data })

            json_str = json.dumps(data)
            print("node_room: ", node_room)
            print("node_name: ", node_name)
            print("transfer node", t_node)
            #print("********************")
            #print(json_str)
            #print("********************")

            #for item in data:
            #    print item["node_name"]
            #    print item["tn_data"]
            #    print
            #    print

            return render(request, 'data_show/show_data.html', {"data": json_str})
        else:
            form = NodeForm()
            return render(request, 'data_show/index.html', {'form': form})

    return render(request, 'data_show/index.html')

def line_chart(request):
    return render(request, 'data_show/line_chart.html')

def test_chart(request):
    return render(request, 'data_show/test.html')

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

def test_data_csv(request):
    fd = open('./data_show/data/readme.csv', 'r')
    data = HttpResponse(fd.read())
    fd.close()

    return data
