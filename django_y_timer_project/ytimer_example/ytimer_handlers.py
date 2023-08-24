
import ytimer
import random

from django.utils import timezone


TIMEOUT = 'TIMEOUT'
POLL_STATUS = 'POLL_STATUS'


@ytimer.timer_handler(type=TIMEOUT)
def process_TIMEOUT(timer):
    from .models import Task

    try:
        task = Task.objects.get(timeout_timer_id=timer.id)
        task.on_timeout()

        timer.done()
    except Task.DoesNotExist:
        timer.done()


@ytimer.timer_handler(type=POLL_STATUS)
def process_many_time_job_example(timer):
    from .models import Task

    try:
        task = Task.objects.get(poll_status_timer_id=timer.id)
        # in real example, poll status from another system
        score = random.randint(1, 100)

        if score >= 90 and score < 95:
            task.on_fail()
            timer.done()
        elif score >= 95:
            task.on_success()
            timer.done()
        else:
            timer.reschedue(timezone.now() + timezone.timedelta(seconds=1))

    except Task.DoesNotExist:
        timer.done()

