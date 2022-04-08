from datetime import datetime
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Song, Vtuber, Group


def Home(request):
    return render(request, 'index.html')


def Index(request):
    # TODO: 撈資料 & 改順序
    songs = Song.objects.all
    # TODO: 放入表頭標籤eg. 排名、歌曲名稱...
    thead_tags = []

    return render(request, 'songs/index.html', {
        'songs': songs,
        'thead_tags': thead_tags
    })
