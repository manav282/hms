from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('register/',views.register,name="register"),
    path('login/',views.login,name='login'),
    path('verify/',views.verify,name='verify'),
    path('uprofile',views.uprofile,name='uprofile'),
    path('profile',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
]