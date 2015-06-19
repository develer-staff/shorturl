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

import re
import urllib2

import models
import settings

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django import forms
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import RequestContext

from settings import ABSOLUTE_PREFIX_JSONP_SERVICE

from django.db import IntegrityError

class UrlForm(forms.Form):
    url = forms.URLField()
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
        return render_to_response('surl/root.html', ctx, context_instance=RequestContext(request))

def redirect(request, url):
    su = get_object_or_404(models.ShortUrl, pk=url)
    ctx = {
        'title': su.title,
        'url': su.url,
        #'ga': settings.GOOGLE_ANALYTICS,
    }
    return render_to_response('surl/redirect.html', ctx, context_instance = RequestContext(request))

def jsonp_short_url(request):
    try:
        url = request.GET['q']
    except KeyError:
        return HttpResponseBadRequest(content='invalid request')
    try:
        title = request.GET['t']
    except KeyError:
        title = None
    return HttpResponse(content='document.log("%s");' % make_short_url(url, title=title))

def make_short_url(url, code=None, reuse=True, title=None):
    short = None
    if reuse:
        try:
            short = models.ShortUrl.objects.filter(url=url)[0]
        except IndexError:
            pass
    if short is None:
        if title is None:
            title = fetch_title(url)
        if code:
            short = models.ShortUrl.new_url(url, title, id=code)
        else:
            short = models.ShortUrl.new_url(url, title)
    if settings.ABSOLUTE_PREFIX_REDIRECT_SERVICE:
        url = settings.ABSOLUTE_PREFIX_REDIRECT_SERVICE + short.id
    else:
        url = reverse('surl-redirect', kwargs={'url': short.id})
    return url

_title = re.compile(r'<title>([^<]*)')

def fetch_title(url):
    try:
        f = urllib2.urlopen(url)
    except:
        return ''
    data = f.read(512)
    f.close()
    match = _title.search(data)
    if not match:
        return ''
    else:
        return match.group(1)
