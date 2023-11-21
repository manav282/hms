from django.urls import path
from . import views
urlpatterns=[
    path('addpres/',views.addpres,name='addpres'),
    path('pres/',views.pres,name='pres'),
    path('history/',views.history,name='history'),
]