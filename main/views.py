from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum, Max

from main.models import GameScore;
from main.forms import CreateContactForm, MassEmailForm;

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
    form = CreateContactForm();
    context = {
        'form': form,
    }
    return render(request, 'main/create_contact.html', context)

def mass_mail(request):
    if request.method == 'POST':
        form = MassEmailForm(request.POST)
        if (form.is_valid()): print(form.cleaned_data['content'])

    form = MassEmailForm(initial = {'content': '<b>yes<b>'});
    context = {
        'form': form,
    }
    return render(request, 'main/create_contact.html', context)