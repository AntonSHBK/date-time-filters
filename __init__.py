# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import django

__author__ = "Anton Pisarenko"

if django.VERSION < (3, 2):
    default_app_config = "date-time-filters.apps.DateTimeFilterConfig"


VERSION = __version__
