from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse

from accounts.forms import RegistrationForm, ProfileChangeForm
from main.views import gen_alerts


class SignUp(generic.CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def logout(request):
    auth.logout(request)
    request.session['notify'] = "Successfully Logged Out!"
    return redirect(request.GET['next'])

@login_required
def profile(request):
    context = gen_alerts(request)
    context['user'] = request.user
    return render(request, 'profile.html', context)

@login_required
def update_password(request):
    form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            request.session['notify'] = "Successfully Changed Password!"
            return HttpResponseRedirect(reverse('profile'))

    context = {
        'form': form
    }
    return render(request, 'password.html', context)

@login_required
def update_profile(request):
    form = ProfileChangeForm()

    if request.method == 'POST':
        form = ProfileChangeForm(request.POST)
        if form.is_valid():
            user = request.user
            if (form.cleaned_data['email']): user.email = form.cleaned_data['email']
            if (form.cleaned_data['first_name']): user.first_name = form.cleaned_data['first_name']
            if (form.cleaned_data['last_name']): user.last_name = form.cleaned_data['last_name']
            user.save()
            request.session['notify'] = "Successfully Updated Profile!"
            return HttpResponseRedirect(reverse('profile'))

    context = {
        'form': form
    }
    return render(request, 'profile_change.html', context)