# -*- coding: UTF-8 -*-
# Copyright (c) 2010 David Mugnai <dvd@develer.com>
# Copyright (c) 2010 Develer s.r.l. 
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from django.db import models
from django.db.utils import IntegrityError

from datetime import datetime
from random import choice

character_set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'

class ShortUrl(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
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
                except IntegrityError, e:
                    pass
                else:
                    break
        else:
            i.id = id
            i.save(force_insert=True)
        return i
