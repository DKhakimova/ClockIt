from django.urls import path
from . import views

urlpatterns = [
  path('', views.index),
  path('registration', views.registration_page),
  path('register', views.register),
  path('pinpad', views.pinpad),
  path('pin_verification', views.pin_verification),
  path('login', views.login),
  path('logout', views.logout)
]