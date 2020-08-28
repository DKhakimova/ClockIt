from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Company, User
import uuid

def newCompany(request):
    return render(request, 'create_company.html')


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
