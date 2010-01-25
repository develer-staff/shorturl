# -*- coding: UTF-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try:
    GOOGLE_ANALYTICS = settings.SURL_GOOGLE_ANALYTICS
except AttributeError:
    raise ImproperlyConfigured('google analytics code not found')

