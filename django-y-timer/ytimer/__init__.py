
from django.conf import settings

from .service import schedule, cancel, timer_handler


def init():
    for app in settings.INSTALLED_APPS:
        try:
            __import__(app + '.ytimer_handlers')
        except ImportError:
            pass

init()