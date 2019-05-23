from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name = 'signup'),
    path('logout/', views.logout, name = 'logout'),
    path('profile/', views.profile, name = 'profile'),
    path('password/', views.update_password, name = 'password')
]