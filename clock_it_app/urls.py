from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('timeclock', views.timeclock),
    path('timecard', views.user_timecard),
    path('clock_in', views.clock_in),
    path('clock_out', views.clock_out),
]