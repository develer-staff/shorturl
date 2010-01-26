# -*- coding: UTF-8 -*-
import re
import urllib2

import models
import settings

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def redirect(request, url):
    su = get_object_or_404(models.ShortUrl, pk=url)
    ctx = {
        'title': su.title,
        'url': su.url,
        'ga': settings.GOOGLE_ANALYTICS,
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
