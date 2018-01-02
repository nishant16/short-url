# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Check(models.Model):
    short_id = models.SlugField(max_length=6, null=True, blank=True)
    http_url = models.URLField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.http_url

