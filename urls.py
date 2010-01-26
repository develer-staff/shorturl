# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'^$', 'shorturl.views.root'),
     (r'', include('surl.urls')),
)
