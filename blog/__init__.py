from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

__all__ = ('celery_app',)
