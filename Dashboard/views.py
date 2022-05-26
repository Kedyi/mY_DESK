from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from .models import *
from .detectorr import *
from .E_Attendance import *
from .import_attendance import *
from .login_list import *


Face_authentication = Face_authentication()

#home page:index

def index(request):
  return render(request,'index.html')

################################## ADMIN AREA ################################################

#admin login

def admin_login(request):
    check = ""
    if request.method == "POST":
      u = request.POST['username']
      p = request.POST['pwd']
      user = authenticate(username=u, password=p)
      try:
        if user.is_staff:
          login(request, user)
          check = "no"
        else:
          check = "yes"
      except:
        check = "yes"
    return render(request, 'admin_login.html', locals())

#admin homepage

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

#employee details on admin_dashboard

def emp_detail(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    employee = UserProfile.objects.all()
    return render(request,'emp_detail.html',locals())

#edit profile for employees on admin dashboard

def edit_profile(request,pid):
  if not request.user.is_authenticated:
    return redirect('admin_login')

  check = ""
  employee = UserProfile.objects.get(face_id=pid)
  if request.method == "POST":
    fn = request.POST['firstname']
    ln = request.POST['lastname']
    dept = request.POST['department']
    designation = request.POST['designation']
    contact = request.POST['contact']
    jdate = request.POST['jdate']
    gender = request.POST['gender']

    employee.user.first_name = fn
    employee.user.last_name = ln
    employee.empdept = dept
    employee.designation = designation
    employee.contact = contact
    employee.gender = gender

    if jdate:
        employee.joiningdate = jdate


    try:
       employee.save()
       employee.user.save()
       check = "no"
    except:
       check = "yes"

  return render(request,'edit_profile.html',locals())

#delete employee from admin dashboard

def delete_employee(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('emp_detail')

# check attendance from the admin_dashboard

def attendance(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    create_attendance()
    return render(request,'Attendance.html')

#track the login activities from admin dashboard

def employee_track(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    call()
    return render(request,'output.html')

#password change for admin dashboard

def password_change_admin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    check=""
    user = request.user
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            if user.check_password(c):
                user.set_password(n)
                user.save()
                check="no"

            else:
                check="not"
        except:
             check: "yes"
    return render(request,'password_change_admin.html',locals())


################################# New employee Sign-up ##############################
def emp_signup(request):
  check = ""
  if request.method == "POST":
    fn = request.POST['firstname']
    ln = request.POST['lastname']
    ec = request.POST['face_id']
    em = request.POST['email']
    pwd = request.POST['pwd']
    try:
       user= User.objects.create_user(first_name=fn, last_name=ln, username=em, password=pwd)
       UserProfile.objects.create(user=user, face_id=ec)
       Face_register(request.POST['face_id'])
       check = "no"
    except:
       check = "yes"

  return render(request,'emp_signup.html',locals())

# get face id during registration

def Face_register(face_id):
    face_id = face_id
    Face_authentication.Detectfaces(face_id)
    Face_authentication.traindata()
    return redirect('/')


######################################## Employee login ####################################

#login using username_password_faceid

def employee_login(request):
    check = ""
    if request.method == "POST":
        u = request.POST['emailid']
        p = request.POST['password']
        f = request.POST['face_id']
        user = authenticate(username=u, password=p)
        if user:
            if (int(Face_authentication.recognizeFace()) == int(f)):
                login_list(u,f)
                login(request, user)
                check = "no"
            else:
                check = "yes"
        else:
            check = "yes"
    return render(request, 'employee_login.html', locals())

#employee homepage

def employee_dashboard(request):
    return render(request, 'employee_dashboard.html')

#employee profile in employee dashboard
#can be edited

def employee_profile(request):
    if not request.user.is_authenticated:
        return redirect('employee_login')

    check = ""
    user = request.user
    employee = UserProfile.objects.get(user=user)
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        dept = request.POST['department']
        designation = request.POST['designation']
        contact = request.POST['contact']
        jdate = request.POST['jdate']
        gender = request.POST['gender']

        employee.user.first_name = fn
        employee.user.last_name = ln
        employee.empdept = dept
        employee.designation = designation
        employee.contact = contact
        employee.gender = gender

        if jdate:
            employee.joiningdate = jdate

            # image also if data present then only update otherwise same

        try:
            employee.save()
            employee.user.save()
            check = "no"
        except:
            check = "yes"

    return render(request, 'employee_profile.html', locals())

#password change for employee

def password_change(request):
    if not request.user.is_authenticated:
        return redirect('employee_login')

    check=""
    user = request.user
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            if user.check_password(c):
                user.set_password(n)
                user.save()
                check="no"

            else:
                check="not"
        except:
             check: "yes"
    return render(request,'password_change.html',locals())

###################################### logout ###############################################

def Logout(request):
    logout(request)
    return redirect('index')