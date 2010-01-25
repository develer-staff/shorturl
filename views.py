# -*- coding: UTF-8 -*-
from django import forms
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import RequestContext

class UrlForm(forms.Form):
    url = forms.URLField(verify_exists=False)
    name = forms.CharField(max_length=6, required=False)

def root(request):
    if request.method == 'POST':
        f = UrlForm(request.POST)
        if f.is_valid():
            return HttpResponse(content = 'x')
        else:
            return HttpResponseBadRequest(content='invalid request')
    else:
        return render_to_response( 'root.html', {'x': UrlForm()}, context_instance = RequestContext(request))
