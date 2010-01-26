# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^short_url$', 'surl.views.jsonp_short_url', name='surl-jsonp-short-url'),
    url(r'^(?P<url>.*)$', 'surl.views.redirect', name = 'surl-redirect'),
)

