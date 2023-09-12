from django.conf import settings
from django.urls import reverse

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "url": reverse,
            "settings": settings,
        }
    )
    return env
