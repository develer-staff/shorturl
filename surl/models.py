# -*- coding: UTF-8 -*-
from django.db import models

from datetime import datetime
from random import choice

character_set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'

class ShortUrl(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    url = models.URLField(verify_exists=False, db_index=True)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def new_url(cls, url, title='', id=None):
        def r():
            return ''.join(choice(character_set) for x in range(4))

        i = ShortUrl()
        i.url = url
        i.title = title
        i.created = datetime.now()
        if id is None:
            while True:
                i.id = r()
                try:
                    i.save(force_insert=True)
                except Exception, e:
                    print e
                else:
                    break
        else:
            i.id = id
            i.save(force_insert=True)
        return i
