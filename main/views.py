import html2text
import time
import math

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum, Max
from django.views import generic
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator

from main.models import GameScore, Meeting, EmailAddress, MassEmail, ContactNotificant, Alert, GameBring
from main.models import QuoteOfDay, VideoOfDay, GameOfWeek
from main.forms import CreateContactForm, MassEmailForm, AddMailForm, ModifyMailForm, DeleteMailForm, TestEmailForm, GameBringForm

def gen_alerts(request):
    """Function for generating banner alerts."""
    # NOTIFICATION MESSAGES (e.g. email successfully added!)
    context = {}
    if (request.session.get('notify')):
        context['notify'] = request.session.get('notify')
        try:
            del request.session['notify']
        except KeyError:
            pass

    # ALERT MESSAGES (e.g. meeting is moved to a new location next week!)
    # displays only unacknowledged alert messages if user is logged in
    if request.user.is_authenticated:
        messages = Alert.objects.filter(time__gt = timezone.now()).exclude(seen__in = [request.user])[0:3]
    else:
        messages = Alert.objects.filter(time__gt = timezone.now())[0:3]
    context['messages'] = messages

    return context

def get_next_meeting():
    """Function for getting the next future meeting."""
    meetings = Meeting.objects.filter(time__gt = timezone.now())
    if meetings:
        return(meetings[0])
    else:
        return None

def alert_update(request):
    """Function for acknowledging alert messsages."""
    if request.method == "GET":
        if request.GET.get('id') and request.user.is_authenticated:
            message = Alert.objects.get(pk = request.GET.get('id'))
            if message:
                message.seen.add(request.user)
                message.save()
    return redirect(request.GET['next'])

# Create your views here.
def index(request):
    """View function for home page of site."""
    context = gen_alerts(request)


    # finds quote to display
    quotes = QuoteOfDay.objects.filter(time__lt = timezone.now())
    if quotes:
        quote = quotes[0]
        context['quote'] = quote

    # finds video link to display
    videos = VideoOfDay.objects.filter(time__lt = timezone.now())
    if videos:
        video = videos[0]
        context['video'] = video

    return render(request, 'index.html', context)

def space_game(request):
    """View function for the space game."""
    context = gen_alerts(request)

    # update scores in the database
    if request.method == "POST":
        if request.POST.get('score'):
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

    # finds drifters destroyed across the site
    drifters_destroyed = GameScore.objects.aggregate(Sum('drifters'))['drifters__sum']
    if (not drifters_destroyed): drifters_destroyed = 0

    # finds the highest score across the site
    site_best = GameScore.objects.aggregate(Max('score'))['score__max']
    if (not site_best): site_best = 0

    context['drifters']  = drifters_destroyed
    context['site_best'] = site_best

    # displays personal best if user is logged in
    if (request.user.is_authenticated):
        personal_scores = GameScore.objects.filter(player__username = request.user.username)
        personal_best = personal_scores.aggregate(Max('score'))['score__max']
        if (not personal_best): personal_best = 0
        context['personal_best'] = personal_best

    return render(request, 'main/space_game.html', context)

def contact(request):
    """View function for creating contact forms."""
    context = gen_alerts(request)

    # adds contact form into the database
    if request.method == "POST":
        form = CreateContactForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit = True)
            if (model_instance.email):
                subject = f'New Contact Request Made by {model_instance.email}'
            else:
                subject = f'New Anonymous Contact Request'

            # sends an email concerning the contact form to selected club officers
            recipients = ContactNotificant.objects.all().values_list('email', flat = True)
            send_mail(
                subject        = subject,
                message        = model_instance.message,
                from_email     = 'Game Night Notifications',
                recipient_list = list(recipients)
            )
            request.session['notify'] = "Contact Successfully Sent!"
            return HttpResponseRedirect(reverse('index'))

    else:
        form = CreateContactForm();

    context['form'] = form
    return render(request, 'main/create_contact.html', context)

@permission_required('main.can_send_emails')
def mass_mail(request):
    """View function for creating mass emails."""
    context = gen_alerts(request)
    next_meeting = get_next_meeting()

    # displays email content if email was already sent
    if (next_meeting and next_meeting.email and next_meeting.email.is_sent):
        message = next_meeting.email
        context['time']    = message.last_edit
        context['subject'] = message.subject
        context['content'] = message.content
        return render(request, 'main/mass_mail_sent.html', context)
    # display nothing if the next meeting is not scheduled
    elif not next_meeting:
        context['no_meeting'] = True

    # creates/saves mass email into the database
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
                context['notify'] = "Email Successfully Saved!"
            elif (next_meeting):
                email = next_meeting.email
                email.subject   = form.cleaned_data['subject']
                email.content   = form.cleaned_data['content']
                email.editor    = request.user
                email.last_edit = timezone.now()
                email.save()
                context['notify'] = "Email Successfully Saved!"

        # checks if mass email is to be saved and sent
        if (request.POST.get('submit', False)):
            return HttpResponseRedirect(reverse('mass_mail_submit'))

        # checks if mass email is to be sent to a test email
        if (request.POST.get('test', False)):
            return HttpResponseRedirect(reverse('mass_mail_test'))

    else:
        if (next_meeting and next_meeting.email):
            message = next_meeting.email
            form    = MassEmailForm(initial = {'subject': message.subject, 'content': message.content})
        else:
            form = MassEmailForm()

    context['form'] = form
    return render(request, 'main/mass_mail.html', context)

@permission_required('main.can_send_emails')
def mass_mail_submit(request):
    """View function for confirming and sending mass emails."""
    FRAGMENT_SIZE = 50 # number of recipients for each email batch: DO NOT SET HIGHER THAN 100
    context = gen_alerts(request)
    next_meeting = get_next_meeting()

    if (not next_meeting or not next_meeting.email or next_meeting.email.is_sent):
        raise Http404("message does not exist")

    message = next_meeting.email
    if request.method == 'POST':
        if (request.POST.get('submit', False)):
            # sends the mass email to all email addresses in the database
            addresses = EmailAddress.objects.all()
            num_recipients = addresses.count()
            recipients = addresses.values_list('email', flat = True)
            plain_text_content = html2text.html2text(message.content)
            tracker = 0
            # send emails by batch
            while tracker < num_recipients:
                recipient_batch = recipients[tracker:(tracker + FRAGMENT_SIZE)]
                mail = EmailMultiAlternatives(
                   subject             = message.subject,
                   body                = plain_text_content,
                   from_email          = 'Game Night',
                   bcc                 = list(recipient_batch),
                   to                  = ['Game Night Members']
                )
                mail.attach_alternative(message.content, "text/html")
                mail.send()
                tracker += FRAGMENT_SIZE
            # signal that the email was sent
            message.is_sent = True
            message.save()
            request.session['notify'] = "Email Successfully Sent!"
            return HttpResponseRedirect(reverse('mass_mail'))
        elif (request.POST.get('back', False)):
            return HttpResponseRedirect(reverse('mass_mail'))

    return render(request, 'main/mass_mail_submission.html', context)

@permission_required('main.can_send_emails')
def mass_mail_test(request):
    """View function for sending a mass email test (sends the mass email to a selected email address)."""
    context = gen_alerts(request)
    next_meeting = get_next_meeting()

    if (not next_meeting or not next_meeting.email):
        raise Http404("message does not exist")

    message = next_meeting.email
    if request.method == 'POST':
        # sends the test email
        form = TestEmailForm(request.POST)
        if (form.is_valid()):
            send_mail(
                subject             = message.subject,
                message             = html2text.html2text(message.content),
                html_message        = message.content,
                from_email          = 'Game Night',
                recipient_list      = [form.cleaned_data['recipient']]
            )
            request.session['notify'] = "Test Email Successfully Sent!"
            return HttpResponseRedirect(reverse('mass_mail'))

    else:
        form = TestEmailForm()

    context['form'] = form
    return render(request, 'main/mass_mail_test.html', context)

def email_list_index(request):
    """Index view function for adding, modifying, or deleting emails."""
    context = gen_alerts(request)
    return render(request, 'main/email_list_index.html', context)

def time_location(request):
    """View function for viewing future meeting times and locations."""
    context = gen_alerts(request)
    active_meetings = Meeting.objects.filter(time__gt = timezone.now())[0:10]
    context['meeting_list'] = active_meetings

    if (active_meetings):
        context['next_meeting'] = get_next_meeting()

    return render(request, 'main/time_location.html', context)

def add_email(request):
    """View function for adding an email address."""
    context = gen_alerts(request)
    if request.method == 'POST':
        form = AddMailForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['new_mail']
            name  = form.cleaned_data['name']
            EmailAddress.objects.create(email = email, name = name)
            request.session['notify'] = "Email Successfully Added!"
            return HttpResponseRedirect(reverse('email_list_index'))

    else:
        form = AddMailForm();

    context['form'] = form
    return render(request, 'main/email_list_add.html', context)

def modify_email(request):
    """View function for modifying an existing email address."""
    context = gen_alerts(request)
    if request.method == 'POST':
        form = ModifyMailForm(request.POST)

        if form.is_valid():
            old_mail = form.cleaned_data['old_mail']
            new_mail = form.cleaned_data['new_mail']
            mail = EmailAddress.objects.filter(email = old_mail)[0]
            mail.email = new_mail
            mail.save()
            request.session['notify'] = "Email Successfully Modified!"
            return HttpResponseRedirect(reverse('email_list_index'))

    else:
        form = ModifyMailForm();

    context['form'] = form
    return render(request, 'main/email_list_modify.html', context)

def delete_email(request):
    """View function for deleting an email address."""
    context = gen_alerts(request)
    if request.method == 'POST':
        form = DeleteMailForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['delete_mail']
            EmailAddress.objects.filter(email = email).delete()
            request.session['notify'] = "Email Successfully Deleted!"
            return HttpResponseRedirect(reverse('email_list_index'))

    else:
        form = DeleteMailForm();

    context['form'] = form
    return render(request, 'main/email_list_delete.html', context)

def random(request):
    """View function for a variety of `random` generators."""
    context = gen_alerts(request)
    context['initial_num'] = math.floor(time.time())
    return render(request, 'main/random.html', context)

def experimental(request):
    """View function for experimental features."""
    context = gen_alerts(request)
    return render(request, 'main/experimental.html', context)

def games(request):
    """View function for games to be brought to the next meeting."""
    context = gen_alerts(request)
    next_meeting = get_next_meeting()

    # checks if the next meeting is set
    if next_meeting and next_meeting.gamebring_set.count() > 0:
        game_set = next_meeting.gamebring_set.all()
        # paginates the GameBring model objects
        paginator = Paginator(game_set, 20)
        page = request.GET.get('page')
        game_page = paginator.get_page(page)
        context['games'] = game_page.object_list
        context['page_obj']  = game_page
    elif not next_meeting:
        context['no_meeting'] = True

    # displays the `game of the week`
    game_of_week_collection = GameOfWeek.objects.filter(time__lt = timezone.now())
    if game_of_week_collection:
        game_of_week = game_of_week_collection[0]
        context['game_of_week'] = game_of_week

    return render(request, 'main/games.html', context)

def game_bring(request):
    """View function for creating a game to be brought to the next meeting."""
    context = gen_alerts(request)
    next_meeting = get_next_meeting()

    if (not next_meeting):
        raise Http404("next meeting not scheduled")

    # saves the game to be brought into the database
    if request.method == 'POST':
        form = GameBringForm(request.POST)

        if form.is_valid():
            GameBring.objects.create(
                game = form.cleaned_data['game'],
                person = form.cleaned_data['person'],
                meeting = next_meeting,
            )
            request.session['notify'] = "Game Successfully Added!"
            return HttpResponseRedirect(reverse('games'))

    else:
        form = GameBringForm()

    context['form'] = form
    return render(request, 'main/game_form.html', context)
