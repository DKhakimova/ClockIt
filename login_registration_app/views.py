from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from clock_it_app.models import Company
import bcrypt


def index(request):
  context = {
    'users': User.objects.all(),
  }
  return render(request, 'login.html', context)

def registration_page(request):
      return render(request, 'registration.html')

def register(request):
  errors = User.objects.validate(request.POST)

  if errors:
    for values in errors.values():
      messages.error(request, values)
    return redirect('/')
  else:

    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    User.objects.create(
      first_name = request.POST['first'],
      last_name = request.POST['last'],
      email = request.POST['email'],
      password = pw_hash,
    )
    messages.success(request, 'You have successfully registered! Please sign in to continue.')
    return redirect('/')


def login(request):
  if request.method == 'POST':
    results = User.objects.filter(email=request.POST['email'])
    if len(results) > 0:
        if bcrypt.checkpw(request.POST['password'].encode(), results[0].password.encode()):
            request.session['user_id'] = results[0].id
            request.session["name"] = (f"{results[0].first_name} {results[0].last_name}")
            return redirect('/account')
            
        else:
            messages.error(request, "Email or password did not match.")
            return redirect("/")
    else:
        messages.error(request, "Email or password did not match.")
        return redirect("/")


def pinpad(request):
   return render(request, 'pin.html')


def pin_verification(request):
  if request.method == "POST":
    print('testing')
    user = User.objects.filter(pin=request.POST['pin']).first()
    if user:
      request.session['user_id'] = user.id
      request.session["name"] = (f"{user.first_name} {user.last_name}")
      return redirect("/account/timeclock")
  return redirect("/pin")

def logout(request):
  request.session.flush()
  return redirect('/')
