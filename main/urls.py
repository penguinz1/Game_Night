from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('contact', views.contact, name = 'contact'),
    path('mass-mail', views.mass_mail, name = 'mass_mail'),
    path('email-list-index', views.email_list_index, name = 'email_list_index'),
    path('time-and-location', views.time_location, name = 'time_location'),
]