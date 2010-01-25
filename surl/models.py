# -*- coding: UTF-8 -*-
from django.db import models

from random import choice

class ShortUrl(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    url = models.URLField(verify_exists=False, db_index=True)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def new_url(cls, url, title=''):
        character_set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'
        def r():
            return ''.join(choice(character_set) for x in range(6))

        i = ShortUrl()
        i.url = url
        i.title = title
        while True:
            i.id = r()
            try:
                i.save()
            except Exception, e:
                print e
            else:
                break
        return i
