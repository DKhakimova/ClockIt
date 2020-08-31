from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime
from time import strftime
from django.contrib import messages
from .models import Company, Timesheet
from login_registration_app.models import User
import random

def new_company(request):
    return render(request, 'create_company.html')

def timeclock(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    if not user.company:
        return redirect('/success')

    timesheet = Timesheet.objects.filter(employee=user).last()
    if timesheet:
        timesheet.clock_in_time = timesheet.clock_in_time.strftime("%I:%M %p %B %d, %Y")
        if timesheet.clock_out_time:
            timesheet.clock_out_time = timesheet.clock_out_time.strftime("%I:%M %p %B %d, %Y")
    context = {
        'timesheet': timesheet,
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'time_clock.html', context)

def user_timecard(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')

    authenticated_user = User.objects.get(id=request.session['user_id'])
    clicked_user = User.objects.get(id=user_id)
    all_timesheets = Timesheet.objects.filter(employee=clicked_user)
    for timesheet in all_timesheets:
        timesheet.date = timesheet.clock_in_time.strftime("%B %d, %Y")
        timesheet.hours = None
        if timesheet.clock_out_time:
            timesheet.hours = (timesheet.clock_out_time - timesheet.clock_in_time).total_seconds()/3600
            timesheet.hours = round(timesheet.hours, 2)
            timesheet.clock_out_time = timesheet.clock_out_time.strftime("%I:%M %p")
        timesheet.clock_in_time = timesheet.clock_in_time.strftime("%I:%M %p")

    context = {
        'all_timesheets': all_timesheets,
        'authenticated_user': authenticated_user,
        'clicked_user': clicked_user
    }

    return render(request, 'user_timecard.html', context)

def clock_in(request):
    if 'user_id' not in request.session:
        return redirect('/')

    users = User.objects.all()
    Timesheet.objects.create(
        employee = User.objects.get(id=request.session['user_id'])
    )
    return redirect("/account/timeclock")
    
def clock_out(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    timesheet = Timesheet.objects.filter(employee=user).last()
    timesheet.clock_out_time = datetime.now()
    timesheet.save()
    return redirect("/account/timeclock")

def add_user_to_company(request):
    company = Company.objects.get(code=request.POST['code'])
    user = User.objects.get(id=request.session['user_id'])
    print('\n\n', company, '\n\n\n')
    user.company = company
    user.save()
    return redirect("/account/timeclock")

def create_company(request):
    errors = Company.objects.validate(request.POST)
    if errors:
        for field, value in errors.items():
            messages.error(request, value, extra_tags='new')
            return redirect('/account/company/new')
    # user = User.objects.get(id=request.session['user_id'])
    n = request.POST.copy()
    # n['user'] = user
    company = Company.objects.company_create(n)
    # when user creates company, they become an admin
    user = User.objects.get(id=request.session['user_id'])
    user.admin = True
    user.company = company
    user.save()
    return redirect('/account/company/' + str(company.id))


def view_company(request, company_id):
    context = {
        'company': Company.objects.get(id=company_id)
    }
    return render(request, 'view_company.html', context)

def generate_code(request, company_id):
    company = Company.objects.get(id=company_id)
    company.code = random.randint(100000, 999999)
    company.save()
    return redirect('/account/company/' + str(company.id))


def time_entry_dashboard(request, company_id):
    company = Company.objects.get(id=company_id)
    user = User.objects.filter(id=request.session['user_id'])
    users = User.objects.filter(company=company).filter(admin=False)
    # add last_timesheet_status to each user at runtime
    for user in users:
        last_timesheet_status = Timesheet.objects.filter(employee=user).last()
        if last_timesheet_status:
            if last_timesheet_status.clock_out_time:
                user.last_timesheet_status = 'Last clocked out at ' + \
                    str(last_timesheet_status.clock_out_time.strftime("%I:%M %p"))
            else:
                user.last_timesheet_status = 'Currently clocked in'
        else:
            user.last_timesheet_status = 'Employee has not yet clocked in'
    context = {
        'company': company,
        'users': users
    }
    return render(request, 'time_entry_dashboard.html', context)
