from datetime import datetime
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Song, Vtuber, Group


def Home(request):
    return render(request, 'index.html')
