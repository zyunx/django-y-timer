from django.db import models

from ool import VersionField, VersionedMixin


class Timer(VersionedMixin, models.Model):
    STATUS_QUEUING = 'queuing'
    STATUS_DONE = 'done'
    STATUS_PROCESSING = 'processing'
    STATUS_NO_HANDLER = 'no_handler'
    STATUS_EXCEPTION = 'exception'
    STATUS_CANCEL = 'cancel'
    STATUS_CHOICES = (
        (STATUS_QUEUING, STATUS_QUEUING),
        (STATUS_DONE, STATUS_DONE),
        (STATUS_PROCESSING, STATUS_PROCESSING),
        (STATUS_NO_HANDLER, STATUS_NO_HANDLER),
        (STATUS_EXCEPTION, STATUS_EXCEPTION),
        (STATUS_CANCEL, STATUS_CANCEL),
    )
    id = models.UUIDField(primary_key=True)
    type = models.CharField(max_length=200)
    data = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_QUEUING)
    schedule_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    version = VersionField()

    
    def __str__(self):
        return self.type + ': ' + str(id)


    def log(self, content):
        TimerLog.objects.create(timer=self, content=content)


    def signal(self, type):
        TimerSignal.objects.create(timer=self, type=type)


    def handle_signals(self):
        for s in self.signals.all():
            if s.type == TimerSignal.TYPE_CANCEL:
                s.status = Timer.STATUS_CANCEL
                self.save()


    def begin_processing(self):
        self.status = Timer.STATUS_PROCESSING
        self.save()


    def no_handler(self):
        self.status = Timer.STATUS_NO_HANDLER
        self.save()


    def done(self):
        self.status = Timer.STATUS_DONE
        self.save()


    def reschedue(self, at):
        self.status = Timer.STATUS_QUEUING
        self.schedule_at = at
        self.save()


    def catch_exception(self, reason):
        self.status = Timer.STATUS_EXCEPTION
        self.save()
        self.log({
            'exception': reason
        })


class TimerLog(models.Model):
    timer = models.ForeignKey(Timer, on_delete=models.CASCADE)
    content = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TimerSignal(models.Model):
    TYPE_CANCEL = 'cancel'
    TYPE_CHOICES = (
        (TYPE_CANCEL, TYPE_CANCEL)
    )
    timer = models.ForeignKey(Timer, on_delete=models.CASCADE, related_name='signals')
    type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-id',)

