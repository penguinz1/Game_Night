import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum, Max
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import EmailMessage

from main.models import GameScore, Meeting, EmailAddress;
from main.forms import CreateContactForm, MassEmailForm, AddMailForm, ModifyMailForm, DeleteMailForm;

# Create your views here.
def index(request):
    """View function for home page of site."""
    if request.method == "POST":
        if request.POST['score']:
            if (request.user.is_authenticated):
                GameScore.objects.create(
                    score = request.POST.get('score', 0),
                    drifters = request.POST.get('drifters', 0),
                    player = request.user,
                )
            else:
                GameScore.objects.create(
                    score = request.POST.get('score', 0),
                    drifters = request.POST.get('drifters', 0),
                )

    drifters_destroyed = GameScore.objects.aggregate(Sum('drifters'))['drifters__sum']
    if (not drifters_destroyed): drifters_destroyed = 0

    site_best = GameScore.objects.aggregate(Max('score'))['score__max']
    if (not site_best): site_best = 0

    context = {
        'drifters': drifters_destroyed,
        'site_best': site_best,
    }

    if (request.user.is_authenticated):
        personal_scores = GameScore.objects.filter(player__username = request.user.username)
        personal_best = personal_scores.aggregate(Max('score'))['score__max']
        if (not personal_best): personal_best = 0
        context['personal_best'] = personal_best

    return render(request, 'index.html', context)

def contact(request):
    if request.method == "POST":
        form = CreateContactForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit = True)
            return HttpResponseRedirect(reverse('index'))

    else:
        form = CreateContactForm();

    context = {
        'form': form,
    }
    return render(request, 'main/create_contact.html', context)

def mass_mail(request):
    if request.method == 'POST':
        form = MassEmailForm(request.POST)
        if (form.is_valid()): 
            print(form.cleaned_data['content'])
        if (request.POST.get('submit', False)):
            return HttpResponseRedirect(reverse('mass_mail_submit'))

    form = MassEmailForm(initial = {'content': '<b>yes<b>'});
    context = {
        'form': form,
    }
    return render(request, 'main/mass_mail.html', context)

def mass_mail_submit(request):
    if request.method == 'POST':
        email = EmailMessage('Meeting Next Saturday', 'Good Morning. This is just to inform you that there is a meeting next Saturday.', 
            to=['kathy.ning7@gmail.com'])
        email.send()

    return render(request, 'main/mass_mail_submission.html')

def email_list_index(request):
    return render(request, 'main/email_list_index.html')

def time_location(request):
    active_meetings = Meeting.objects.filter(time__gt = datetime.datetime.now())[0:10]
    context = {
        'meeting_list': active_meetings,
    }

    if (active_meetings):
        context['next_meeting'] = active_meetings[0]

    return render(request, 'main/time_location.html', context)

def add_email(request):
    if request.method == 'POST':
        form = AddMailForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['new_mail']
            name  = form.cleaned_data['name']
            EmailAddress.objects.create(email = email, name = name)
            return HttpResponseRedirect(reverse('email_list_index'))

    else:
        form = AddMailForm();

    context = {
        'form': form,
    }
    return render(request, 'main/email_list_add.html', context)

def modify_email(request):
    if request.method == 'POST':
        form = ModifyMailForm(request.POST)

        if form.is_valid():
            old_mail = form.cleaned_data['old_mail']
            new_mail = form.cleaned_data['new_mail']
            mail = EmailAddress.objects.filter(email = old_mail)[0]
            mail.email = new_mail
            mail.save()
            return HttpResponseRedirect(reverse('email_list_index'))

    else:
        form = ModifyMailForm();

    context = {
        'form': form,
    }
    return render(request, 'main/email_list_modify.html', context)

def delete_email(request):
    if request.method == 'POST':
        form = DeleteMailForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['delete_mail']
            EmailAddress.objects.filter(email = email).delete()
            return HttpResponseRedirect(reverse('email_list_index'))

    else:
        form = DeleteMailForm();

    context = {
        'form': form,
    }
    return render(request, 'main/email_list_delete.html', context)

def experimental(request):
    return render(request, 'main/experimental.html')

def games(request):
    return render(request, 'main/games.html')

def profile(request):
    return render(request, 'main/profile.html')
