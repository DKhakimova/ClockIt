from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime
from time import strftime
from django.contrib import messages
from .models import Company, User, Timesheet
import uuid

def newCompany(request):
    return render(request, 'create_company.html')

def timeclock(request):
    # context = {
    #     'user': User.objects.get(id=request.session['user_id']),
    # }
    timesheet = Timesheet.objects.last()
    timesheet.clock_in_time = timesheet.clock_in_time.strftime("%I:%M %p %B %d, %Y")
    if timesheet.clock_out_time:
        timesheet.clock_out_time = timesheet.clock_out_time.strftime("%I:%M %p %B %d, %Y")
    context = {
        'timesheet': timesheet
    }
    return render(request, 'time_clock.html', context)

def user_timecard(request):
    all_timesheets = Timesheet.objects.all()
    for timesheet in all_timesheets:
        timesheet.date = timesheet.clock_in_time.strftime("%B %d, %Y")
        timesheet.hours = None
        if timesheet.clock_out_time:
            timesheet.hours = (timesheet.clock_out_time - timesheet.clock_in_time).total_seconds()/3600
            timesheet.hours = round(timesheet.hours, 2)
            timesheet.clock_out_time = timesheet.clock_out_time.strftime("%I:%M %p")
        timesheet.clock_in_time = timesheet.clock_in_time.strftime("%I:%M %p")
        
    context = {
    # 'user': User.objects.get(id=request.session['user_id']),
        'all_timesheets': all_timesheets,
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

def createCompany(request):
    errors = Company.objects.validate(request.POST)
    if errors:
        for field, value in errors.items():
            messages.error(request, value, extra_tags='new')
            return redirect('/company/new')
    # user = User.objects.get(id=request.session['user_id'])
    n = request.POST.copy()
    # n['user'] = user
    company = Company.objects.companyCreate(n)
    return redirect('/company/' + str(company.id))


def viewCompany(request, company_id):
    context = {
        'company': Company.objects.get(id=company_id)
    }
    return render(request, 'view_company.html', context)

def generateCode(request, company_id):
    company = Company.objects.get(id=company_id)
    company.code = uuid.uuid4()
    company.save()
    return redirect('/company/' + str(company.id))


def timeEntryDashboard(request, company_id):
    context = {
        'company': Company.objects.get(id=company_id)
    }
    return render(request, 'time_entry_dashboard.html', context)
