# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'^s/', include('surl.urls')),
     (r'', 'shorturl.views.root'),
)
