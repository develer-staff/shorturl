from django.db import models
from django.db.utils import IntegrityError

from datetime import datetime
from random import choice

character_set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'

class ShortUrl(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    url = models.URLField(db_index=True)
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
                except IntegrityError, e:
                    pass
                else:
                    break
        else:
            i.id = id
            i.save(force_insert=True)
        return i
