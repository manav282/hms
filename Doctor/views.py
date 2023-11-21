from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Home.models import Doctor, Patient
from django.contrib.auth.models import User
from .models import Prescription

# Create your views here.


@login_required
def addpres(request):
    doc = Doctor.objects.filter(user=request.user).first()
    p = Patient.objects.all()
    if request.method == 'POST':
        patname = request.POST['pat']
        pres = request.POST['pres']
        us = User.objects.filter(first_name=patname).first()
        pat = Patient.objects.filter(user=us).first()
        dis = request.POST['dis']
        prescript = Prescription(
            prescription=pres, patient=pat, doctor=doc, disease=dis)
        prescript.save()
        return redirect("pres")
    return render(request, 'Doctor/addpres.html', {'p': p})


@login_required
def pres(request):
    pre = Prescription.objects.all()
    return render(request, 'Doctor/pres.html', {'pre': pre})


@login_required
def history(request):
    doc = Patient.objects.filter(user=request.user).first()
    pre = Prescription.objects.filter(patient=doc).all()
    return render(request, 'Doctor/history.html', {'pre': pre})
