# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<url>.*)$', 'surl.views.redirect', name = 'surl-redirect'),
)

