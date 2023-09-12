from .base import *

CSRF_TRUSTED_ORIGINS = []
DEBUG = True

STATIC_ROOT = ""
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
