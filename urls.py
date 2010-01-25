# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'', 'shorturl.views.root'),
     (r'^s/', include('surl.urls')),
)
