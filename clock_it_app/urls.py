from django.urls import path, include
from . import views

urlpatterns = [
    path('timeclock', views.timeclock),
    path('timecard', views.user_timecard),
    path('clock_in', views.clock_in),
    path('clock_out', views.clock_out),
    path('company/new', views.newCompany),
    path('company/create', views.createCompany),
    path('company/<int:company_id>', views.viewCompany),
    path('company/<int:company_id>/generate-code', views.generateCode),
    path('company/<int:company_id>/time-entry-dashboard', views.timeEntryDashboard)
]
