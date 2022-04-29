from django.shortcuts import render
from .models import *


def Index(request):

    template = 'index.html'
    context = {

    }

    return render(request, template, context)
