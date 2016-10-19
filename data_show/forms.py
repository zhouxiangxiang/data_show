
from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)

class NodeForm(forms.Form):
    #node_name = forms.CharField(label="node-name", max_length=100)
    node_room = forms.CharField(label="node_room", max_length=100)
