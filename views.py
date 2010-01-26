# -*- coding: UTF-8 -*-
from django import forms
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import RequestContext

from surl import models
from surl.settings import ABSOLUTE_PREFIX_JSONP_SERVICE
from surl.views import make_short_url

from django.db import IntegrityError

class UrlForm(forms.Form):
    url = forms.URLField(verify_exists=False)
    name = forms.CharField(max_length=4, required=False)
    reuse = forms.BooleanField(required=False)

def root(request):
    if request.method == 'POST':
        f = UrlForm(request.POST)
        if f.is_valid():
            data = f.cleaned_data
            try:
                url = make_short_url(data['url'], code=data['name'], reuse=data['reuse'])
            except IntegrityError, e:
                return HttpResponseBadRequest(content='name already used')
            return HttpResponse(content = url)
        else:
            return HttpResponseBadRequest(content='invalid request')
    else:
        ctx = {
            'jsonp': ABSOLUTE_PREFIX_JSONP_SERVICE,
        }
        return render_to_response('root.html', ctx, context_instance=RequestContext(request))

