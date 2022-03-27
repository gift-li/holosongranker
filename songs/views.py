from datetime import datetime
from django.shortcuts import render


def Home(request):
    return render(request, 'index.html')


def index(request):
    return render(request, 'index', [

    ])
