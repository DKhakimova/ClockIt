from django.contrib import admin
from .models import Timesheet

# Register your models here.

class TimesheetAdmin(admin.ModelAdmin):
    pass

admin.site.register(Timesheet, TimesheetAdmin)


