from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('admin_login/', admin_login, name='admin_login'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('password_change_admin/', password_change_admin, name='password_change_admin'),
    path('emp_detail/', emp_detail, name='emp_detail'),
    path('delete_employee/<int:pid>', delete_employee, name='delete_employee'),
    path('edit_profile/<int:pid>', edit_profile, name='edit_profile'),
    path('attendance/',attendance,name='attendance'),
    path('employee_track/',employee_track,name='employee_track'),
    path('emp_signup/', emp_signup, name='emp_signup'),
    path('employee_login/', employee_login, name='employee_login'),
    path('employee_dashboard/', employee_dashboard, name='employee_dashboard'),
    path('employee_profile/', employee_profile, name='employee_profile'),
    path('password_change/', password_change, name='password_change'),
    path('Logout/', Logout, name='Logout'),
    ]