from django.shortcuts import render
from datas.models import *


def Index(request):
    template = 'songs/index.html'
    # TODO: 撈資料 & 改順序
    songs = Song.objects.all()[:10]

    context = {
        'songs': songs,
    }

    return render(request, template, context)
