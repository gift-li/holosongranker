from django.shortcuts import render
from datas.models import *
from django.db.models import Max
from pprint import pp


def Index(request):
    # 取得最新總觀看數前n名的songs
    # songs = Song.objects.prefetch_related('sing_songs')[:3]
    songs = Song.objects.annotate(
        latest_total_view=Max('song_records__total_view')
    ).order_by('-latest_total_view')[:5]

    template = 'songs/ranker.html'
    context = {
        'songs': songs,
    }

    return render(request, template, context)
