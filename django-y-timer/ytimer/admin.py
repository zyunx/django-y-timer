from django.contrib import admin

from .models import Timer, TimerLog, TimerSignal

class TimerLogInline(admin.StackedInline):
    model = TimerLog
    extra = 0

class TimerSignalInline(admin.TabularInline):
    model = TimerSignal
    extra = 0

class TimerAdmin(admin.ModelAdmin):
    inlines = [TimerSignalInline, TimerLogInline]

admin.site.register(Timer, TimerAdmin)
