from django.urls import path, include
from . import views

urlpatterns = [
    path('timeclock', views.timeclock),
    path('timecard', views.user_timecard),
    path('clock_in', views.clock_in),
    path('clock_out', views.clock_out),
    path('company/user', views.add_user_to_company),
    path('company/new', views.new_company),
    path('company/create', views.create_company),
    path('company/<int:company_id>/generate-code', views.generate_code),
    path('company/<int:company_id>/time-entry-dashboard', views.time_entry_dashboard),
    path('company/<int:company_id>', views.view_company),
]
