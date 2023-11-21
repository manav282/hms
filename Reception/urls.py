from django.urls import path
from . import views

urlpatterns=[
    path('appointments/',views.appointments,name='appointments'),
    path('deleteapt/',views.deleteapt,name='deleteapt'),
    path('updateapt/',views.updateapt,name='updateapt'),
    path('getapt/',views.getapt,name='getapt'),
    path('reception/',views.reception,name='reception'),
    path('setapt/',views.setapt,name='setapt'),
    path('deletepat/',views.deletepat,name='deletepat'),
    path('updatepat/',views.updatepat,name='updatepat'),
    path('createpat/',views.createpat,name='crtpat'),
]