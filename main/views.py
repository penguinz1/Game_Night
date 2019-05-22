import html2text

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum, Max
from django.views import generic
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.decorators import permission_required, login_required

from main.models import GameScore, Meeting, EmailAddress, MassEmail, ContactNotificant;
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
            if (model_instance.email):
                subject = f'New Contact Request Made by {model_instance.email}'
            else:
                subject = f'New Anonymous Contact Request'

            recipients = ContactNotificant.objects.all().values_list('email', flat = True)
            send_mail(
                subject        = subject,
                message        = model_instance.message,
                from_email     = 'Game Night Notifications',
                recipient_list = list(recipients)
            )
            return HttpResponseRedirect(reverse('index'))

    else:
        form = CreateContactForm();

    context = {
        'form': form,
    }
    return render(request, 'main/create_contact.html', context)

@permission_required('main.can_send_emails')
def mass_mail(request):
    next_meeting = Meeting.objects.filter(time__gt = timezone.now())[0]
    if (next_meeting and next_meeting.email and next_meeting.email.is_sent):
        message = next_meeting.email
        context = {
            'time': message.last_edit,
            'subject': message.subject,
            'content': message.content
        }
        return render(request, 'main/mass_mail_sent.html', context)

    if request.method == 'POST':
        form = MassEmailForm(request.POST)
        if (form.is_valid()): 
            if (next_meeting and not next_meeting.email):
                email = MassEmail.objects.create(
                    subject = form.cleaned_data['subject'],
                    content = form.cleaned_data['content'],
                    editor  = request.user
                )
                next_meeting.email = email
                next_meeting.save()
            elif (next_meeting):
                email = next_meeting.email
                email.subject   = form.cleaned_data['subject']
                email.content   = form.cleaned_data['content']
                email.editor    = request.user
                email.last_edit = timezone.now()
                email.save()


        if (request.POST.get('submit', False)):
            return HttpResponseRedirect(reverse('mass_mail_submit'))

    else:
        if (next_meeting and next_meeting.email):
            message = next_meeting.email
            form    = MassEmailForm(initial = {'subject': message.subject, 'content': message.content})
        else:
            form = MassEmailForm()

    context = {
        'form': form,
    }
    return render(request, 'main/mass_mail.html', context)

@permission_required('main.can_send_emails')
def mass_mail_submit(request):
    next_meeting = Meeting.objects.filter(time__gt = timezone.now())[0]

    if (not next_meeting or not next_meeting.email or next_meeting.email.is_sent):
        raise Http404("message does not exist")

    message = next_meeting.email
    if request.method == 'POST':
        recipients = EmailAddress.objects.all().values_list('email', flat = True)
        send_mail(
           subject             = message.subject,
           message             = html2text.html2text(message.content),
           html_message        = message.content,
           from_email          = 'Game Night',
           recipient_list      = list(recipients)
        )
        message.is_sent = True
        message.save()
        return HttpResponseRedirect(reverse('mass_mail'))

    return render(request, 'main/mass_mail_submission.html')

def email_list_index(request):
    return render(request, 'main/email_list_index.html')

def time_location(request):
    active_meetings = Meeting.objects.filter(time__gt = timezone.now())[0:10]
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

@login_required
def profile(request):
    return render(request, 'main/profile.html')
