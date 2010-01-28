# -*- coding: UTF-8 -*-
# Copyright (c) 2010 David Mugnai <dvd@develer.com>
# Copyright (c) 2010 Develer s.r.l. 
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

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

