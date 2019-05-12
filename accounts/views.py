from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import auth
from django.shortcuts import redirect

from accounts.forms import RegistrationForm


class SignUp(generic.CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def logout(request):
    auth.logout(request)
    return redirect(request.GET['next'])