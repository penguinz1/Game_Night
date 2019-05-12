from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum

from main.models import GameScore;

# Create your views here.
def index(request):
    """View function for home page of site."""
    if request.method == "POST":
        if request.POST['score']:
            print(request.POST['score'])
            GameScore.objects.create(
                score = request.POST.get('score', 0),
                drifters = request.POST.get('drifters', 0),
            )

    drifters_destroyed = GameScore.objects.aggregate(Sum('drifters'))['drifters__sum']
    if (not drifters_destroyed): drifters_destroyed = 0

    context = {
        'drifters': drifters_destroyed,
    }

    return render(request, 'index.html', context)