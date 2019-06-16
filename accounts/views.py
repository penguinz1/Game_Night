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
from django.contrib.auth import update_session_auth_hash

from accounts.forms import RegistrationForm, ProfileChangeForm
from main.views import gen_alerts


class SignUp(generic.CreateView):
    """View for signing up."""
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def logout(request):
    """View for logging out."""
    auth.logout(request)
    return redirect(request.GET['next'])

@login_required
def profile(request):
    """View for the User profile."""
    context = gen_alerts(request)
    context['user'] = request.user
    return render(request, 'profile.html', context)

@login_required
def update_password(request):
    """View for updating User password."""
    context = gen_alerts(request)
    form = PasswordChangeForm(user = request.user)

    # updates the User password in the database.
    if request.method == 'POST':
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            request.session['notify'] = "Successfully Changed Password!"
            return HttpResponseRedirect(reverse('profile'))

    context['form'] = form
    return render(request, 'password.html', context)

@login_required
def update_profile(request):
    """View for updating User profile."""
    context = gen_alerts(request)
    form = ProfileChangeForm()

    # updates the User profile in the database.
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

    context['form'] = form
    return render(request, 'profile_change.html', context)