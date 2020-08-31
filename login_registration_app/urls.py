from django.urls import path
from . import views

urlpatterns = [
  path('', views.index),
  path('success', views.success),
  path('register', views.register),
  path('pin', views.pin),
  path('login', views.login),
  path('logout', views.logout)
]