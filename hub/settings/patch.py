import django
from django.utils.encoding import force_str
from django.utils.translation import gettext, ngettext


def monkey_patching():
    django.utils.encoding.force_text = force_str
    django.utils.translation.ugettext = gettext
    django.utils.translation.ungettext = ngettext
