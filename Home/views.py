from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor
from django.contrib import messages
import datetime
from django.core.mail import send_mail
import random


def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        phone = request.POST['phone']
        typ = request.POST['type']
        if pass1 == pass2:
            if User.objects.filter(username=email).exists():
                messages.info(request, "Email Id already Exists!")
                return redirect('register')
            else:
                o = str(random.randint(100000, 999999))
                global context
                context={'fname':fname,'last_name':typ, 'username':email, 'password':pass1, 'email':email,'phone':phone,'o':o}
                m='Hey '+context['fname']+'!\n'+'Thank you for registering with the Hospital Management!\n\n'+'Your OTP is :'+o
                send_mail('Registration Successful!',m,'Hospital Management',[context['email']],fail_silently=True)
                return redirect('verify')
        else:
            messages.info(request, "Passwords didn't matched!")
            return redirect('register')
    else:
        return render(request, 'register.html')



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            if request.user.last_name == "Reception":
                return redirect('reception')
            if request.user.last_name == "HR":
                return redirect('dashboard')
            if user.last_name == "Doctor":
                pro = Doctor.objects.filter(user=user).first()
                return redirect('profile')
            if user.last_name == "Patient":
                pro = Patient.objects.filter(user=user).first()
                return redirect('profile')
        else:
            messages.info(request, "Invalid Credentials!")
            return redirect('login')
    else:
        return render(request, 'login.html')

def verify(request):
    global context
    if request.method == 'POST' and request.POST.get('submit1') == 'Submit':
        otp = request.POST['otp']
        if context['o'] == otp:
            user = User.objects.create_user(first_name=context['fname'], last_name=context['last_name'], username=context['email'], password=context['password'], email=context['email'])
            if context['last_name'] == "Doctor":
                pro = Doctor(user=user, phone=context['phone'], otp=otp)
                pro.save()
                messages.info(request, "Account Created Successfully")
                return redirect('login')
            if context['last_name'] == "Patient":
                pro = Patient(user=user, phone=context['phone'], otp=otp)
                pro.verify=1
                pro.save()
                messages.info(request, "Account Created Successfully")
                return redirect('login')
            return redirect('login')
        else:
            messages.info(request, "Invalid OTP!")
            return redirect('verify')
    elif request.method == 'POST' and request.POST.get('resend') == 'Resend OTP':
        o = str(random.randint(100000, 999999))
        m='Hey '+context['fname']+'!\n'+'Thank you for registering with the Hospital Management!\n\n'+'Your OTP is :'+o
        send_mail('Registration Successful!',m,'Hospital Management',[context['email']],fail_silently=True)
        return redirect('verify')
    return render(request, 'verify.html')


@login_required
def uprofile(request):
    if request.user.last_name == 'Doctor':
        pro = Doctor.objects.filter(user=request.user).first()
    if request.user.last_name == 'Patient':
        pro = Patient.objects.filter(user=request.user).first()
    if request.user.last_name == 'Reception':
        pid = request.POST['pid']
        pro = Patient.objects.filter(pid=pid).first()
    if request.method == 'POST':
        if request.user.last_name == 'Reception':
            pid = request.POST['pid']
            pro = Patient.objects.filter(pid=pid).first()
        if request.user.last_name == 'HR':
            pid = request.POST['pid']
            pro = Doctor.objects.filter(did=pid).first()
        try:
            _, file = request.FILES.popitem()
            file = file[0]
            pro.image = file
        except:
            pass
        finally:
            pro.phone = request.POST['phone']
            pro.age = request.POST['age']
            pro.gender = request.POST['gender']
            if pro.user.last_name == 'Patient':
                pro.address = request.POST['address']
                pro.casepaper = request.POST['casepaper']
                pro.bloodgroup = request.POST['bloodgroup']
            if pro.user.last_name == 'Doctor':
                pro.status = request.POST['status']
                pro.salary = pro.salary
                pro.Department = request.POST['dept']
                pro.attendance = pro.attendance
            pro.save()
            if request.user.last_name == 'Reception':
                return redirect("reception")
            if request.user.last_name == 'HR':
                return redirect("dashboard")
            return redirect('profile')
    c = {'pro': pro}
    return render(request, 'uprofile.html', c)


@login_required
def profile(request):
    if request.user.last_name == 'Doctor':
        pro = Doctor.objects.filter(user=request.user).first()
    if request.user.last_name == 'Patient':
        pro = Patient.objects.filter(user=request.user).first()
    c = {'pro': pro}
    return render(request, 'profile.html', c)


def logout(request):
    auth.logout(request)
    return redirect('login')
