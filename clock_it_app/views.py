from django.shortcuts import render, redirect, HttpResponse
from . models import Timesheet
from datetime import datetime
from time import strftime

# Create your views here.

def index(request):
    return HttpResponse("hello guys")

def timeclock(request):
    # context = {
    #     'user': User.objects.get(id=request.session['user_id']),
    # }
    timesheet = Timesheet.objects.last()
    # timesheet.clock_in_time = timesheet.clock_in_time.strftime("%I:%M %p" "%B %d, %Y")
    context = {
        'timesheet': timesheet
    }
    return render(request, 'time_clock.html', context)

def user_timecard(request):
    context = {
    #     # 'user': User.objects.get(id=request.session['user_id']),
        'all_timesheets': Timesheet.objects.all()
    }
    return render(request, 'user_timecard.html', context)

def clock_in(request):
    # user = User.objects.get(id=request.session['user_id'])
    Timesheet.objects.create()
    return redirect("/account/timeclock")
    
def clock_out(request):
    timesheet = Timesheet.objects.last()
    timesheet.clock_out_time = datetime.now()
    timesheet.save()
    return redirect("/account/timeclock")