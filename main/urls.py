from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('contact', views.contact, name = 'contact'),
    path('mass-mail', views.mass_mail, name = 'mass_mail'),
    path('email-list-index', views.email_list_index, name = 'email_list_index'),
    path('time-and-location', views.time_location, name = 'time_location'),
    path('email-list-add', views.add_email, name = 'add_email'),
    path('email-list-modify', views.modify_email, name = 'modify_email'),
    path('email-list-delete', views.delete_email, name = 'delete_email'),
    path('experimental', views.experimental, name = 'experimental'),
    path('games', views.games, name = 'games'),
    path('profile', views.profile, name = 'profile'),
]