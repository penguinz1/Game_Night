from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    """View function for home page of site."""

    return render(request, 'index.html')