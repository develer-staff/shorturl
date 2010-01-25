# -*- coding: UTF-8 -*-
from django import forms
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import RequestContext

from surl import models

from django.db import IntegrityError

class UrlForm(forms.Form):
    url = forms.URLField(verify_exists=False)
    name = forms.CharField(max_length=6, required=False)
    reuse = forms.BooleanField(required=False)

def root(request):
    if request.method == 'POST':
        f = UrlForm(request.POST)
        if f.is_valid():
            data = f.cleaned_data
            short = None
            if data['reuse']:
                try:
                    short = models.ShortUrl.objects.filter(url=data['url'])[0]
                except IndexError:
                    pass
            if short is None:
                title = ''
                if data['name']:
                    try:
                        short = models.ShortUrl.new_url(data['url'], title, id=data['name'])
                    except IntegrityError, e:
                        return HttpResponseBadRequest(content='name already used')
                else:
                    short = models.ShortUrl.new_url(data['url'], title)
            return HttpResponse(content = short.id)
        else:
            return HttpResponseBadRequest(content='invalid request')
    else:
        return render_to_response( 'root.html', {}, context_instance = RequestContext(request))

