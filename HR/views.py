from django.shortcuts import render, redirect
from django.contrib import messages
from Home.models import Doctor, Patient
from .models import Payment
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.shortcuts import HttpResponse

# Create your views here.


@login_required
def dashboard(request):
    p = Doctor.objects.all()
    ad = len(Doctor.objects.filter(status="ACTIVE").all())
    tot = len(p)
    k = len(Patient.objects.all())
    c = {'p': p, 'tot': tot, 'k': k, 'ad': ad}
    return render(request, "HR/dashboard.html", c)


@login_required
def deletedoc(request):
    if request.method == 'POST':
        pid = request.POST['pid']
        px = Doctor.objects.filter(did=pid).first()
        us = User.objects.filter(username=px.user.username).first()
        us.delete()
    return redirect("dashboard")


@login_required
def createdoc(request):
    if request.method == 'POST':
        fname = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST['gender']
        age = request.POST['age']
        status = request.POST['status']
        salary = request.POST['salary']
        dept = request.POST['dept']
        attn = request.POST['attn']
        if User.objects.filter(username=email).exists():
            messages.info(request, "Doctor already exists!!")
            return redirect('crtdoc')
        else:
            user = User.objects.create_user(
                first_name=fname, last_name='Doctor', username=email, email=email)
            pro = Doctor(user=user, phone=phone, gender=gender, age=age,
                         status=status, salary=salary, attendance=attn, Department=dept)
            pro.save()
            return redirect('dashboard')
    return render(request, 'HR/crtdoc.html')


@login_required
def updatedoc(request):
    if request.method == 'POST':
        pid = request.POST['pid']
        pro = Doctor.objects.filter(did=pid).first()
        return render(request, 'uprofile.html', {'pro': pro})


@login_required
def accounting(request):
    p = Patient.objects.all()
    if request.method == 'POST':
        pat = request.POST['pat']
        us = User.objects.filter(first_name=pat).first()
        pe = Patient.objects.filter(user=us).first()
        paid = int(request.POST['paid'])
        out = int(request.POST['out'])
        tot = paid+out
        tax = ((0.05)*tot)
        tot = tot+tax
        pay = Payment(patient=pe, paid=paid, outstanding=out, total=tot)
        pay.save()
    payt = Payment.objects.all()
    return render(request, 'HR/accounting.html', {'p': p, 'payt': payt})


@login_required
def send(request):
    if request.method == 'POST':
        pmid = request.POST['pid']
        inv = Payment.objects.filter(pmid=pmid).first()
        m = 'Hey '+str(inv.patient)+'!\n\n'+'Your outstanding billing amount is :'+str(inv.outstanding)+'$\n\n' + \
            'Your Total Billing amount is :' + \
            str(inv.total)+'$\n\n' + \
            'Your Paid Billing amount is :'+str(inv.paid)+'$'
        send_mail('Payment Remainder!', m, 'Hospital Management System', [
                  inv.patient.user.username], fail_silently=True)
        return redirect('accounting')


@login_required
def show(request):
    if request.method == 'POST':
        pmid = request.POST['pid']
        inv = Payment.objects.filter(pmid=pmid).first()
    return render(request, 'HR/show.html', {'inv': inv})

@login_required
def payments(request):
    pat=Patient.objects.filter(user=request.user).first()
    payt=Payment.objects.filter(patient=pat).all()
    return render(request,"HR/payments.html",{'payt':payt})

@login_required
def generatepdf(request):
    if request.method == 'POST':
        pmid = request.POST['pid']
        inv = Payment.objects.filter(pmid=pmid).first()
        html_template = get_template('HR/download.html').render({'inv': inv})

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="invoice.pdf"'

        # Create a PDF document using ReportLab
        pisa_status = pisa.CreatePDF(
            html_template,
            dest=response,
        )

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
