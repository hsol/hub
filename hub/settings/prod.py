from .base import *

CSRF_TRUSTED_ORIGINS = []
DEBUG = False
MIDDLEWARE.append("django.middleware.cache.FetchFromCacheMiddleware")
