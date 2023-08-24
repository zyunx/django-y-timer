
import traceback

from django.utils import timezone

all_handlers = {}

types_for_all_handlers = []


def add_handler(type, handler):
    all_handlers[type] = handler
    types_for_all_handlers.append(type)


def timer_handler(type):
    def add_handler_of_type(func):
        add_handler(type, func)
        return func 
    return add_handler_of_type


def schedule(id, type, data, schedule_at):
    from .models import Timer
    return Timer.objects.create(id=id, type=type, data=data, schedule_at=schedule_at,
                               status=Timer.STATUS_QUEUING)


def cancel(id):
    from .models import Timer, TimerSignal
    try:
        p = Timer.objects.get(id=id)
        p.signal(TimerSignal.TYPE_CANCEL)
    except Timer.DoesNotExist:
        pass


class NoMoreTimerDue(Exception):
    pass


def get_next_timer_for_processing(types):
    import ool
    from .models import Timer

    timer = None
    while timer is None:
        timer = Timer.objects.filter(status=Timer.STATUS_QUEUING,
                                      type__in=types,
                                      schedule_at__lte=timezone.now()).order_by('-schedule_at').first()
        
        if timer is not None:
            try:
                timer.begin_processing()
            except ool.ConcurrentUpdate:
                timer = None
        else:
            raise NoMoreTimerDue()
    return timer


def handle_timer():
    
    timer = get_next_timer_for_processing(types_for_all_handlers)
    
    # handle signals before main processing
    timer.handle_signals()
    if _is_zombie(timer):
        _archive(timer)
        return
    
    try:
        handler = all_handlers.get(timer.type, None)
        if handler == None:
            timer.no_handler()
        else:
            handler(timer)
    except:
        timer.catch_exception({
            'trace': traceback.format_exc()
        })

    # handle signals after main processing
    timer.handle_signals()
    if _is_zombie(timer):
        _archive(timer)


def _is_zombie(timer):
    from .models import Timer

    return timer.status in (Timer.STATUS_DONE, Timer.STATUS_CANCEL)


def _archive(timer):
    timer.delete()
