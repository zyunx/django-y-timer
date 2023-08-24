import uuid
from django.db import models
from django.utils import timezone


class Task(models.Model):
    STATUS_CREATED = 'created'
    STATUS_RUNNING = 'running'
    STATUS_SUCCESS = 'success'
    STATUS_FAIL = 'fail'
    STATUS_TIMEOUT = 'timerout'
    STATUS_CHOICES = (
        (STATUS_CREATED, STATUS_CREATED),
        (STATUS_RUNNING, STATUS_RUNNING),
        (STATUS_SUCCESS, STATUS_SUCCESS),
        (STATUS_FAIL, STATUS_FAIL),
        (STATUS_TIMEOUT, STATUS_TIMEOUT),
    )
    title = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default=STATUS_CREATED)
    timeout_timer_id = models.UUIDField(null=True, blank=True)
    timeout_in_seconds = models.IntegerField(null=True, blank=True)
    poll_status_timer_id = models.UUIDField(null=True, blank=True)


    def run(self):
        import ytimer
        from . import ytimer_handlers
        # maybe request for running on another system
        #self.do_run()

        self.status = Task.STATUS_RUNNING
        self.timeout_timer_id = uuid.uuid4()
        self.poll_status_timer_id = uuid.uuid4()
        self.save()
        
        # poll status timer
        ytimer.schedule(self.poll_status_timer_id,
                        ytimer_handlers.POLL_STATUS,
                        None,
                        timezone.now() + timezone.timedelta(seconds=1))
        # timeout timer
        ytimer.schedule(self.timeout_timer_id,
                        ytimer_handlers.TIMEOUT,
                        None,
                        timezone.now() + timezone.timedelta(seconds=self.timeout_in_seconds))
        

    def on_success(self):
        import ytimer

        self.status = Task.STATUS_SUCCESS
        self.save()
        # cancel timeout
        ytimer.cancel(self.timeout_timer_id)


    def on_fail(self):
        import ytimer

        self.status = Task.STATUS_FAIL
        self.save()
        # cancel timeout
        ytimer.cancel(self.timeout_timer_id)

    
    def on_timeout(self):
        import ytimer

        self.status = Task.STATUS_TIMEOUT
        self.save()
        # cancel poll
        ytimer.cancel(self.poll_status_timer_id)

        


