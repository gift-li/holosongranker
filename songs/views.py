from django.shortcuts import render
from datas.models import *
from django.db.models import Max
from pprint import pp


def Index(request):
    order_query = str('-total_view')
    exclude_group = [Group.Unit.GROUP]
    rank_num_to = 5

    last_song_record_date = Record.objects.values_list(
        'date', flat=True).latest('date')
    records = Record.objects.filter(date=last_song_record_date) \
        .prefetch_related('song', 'song__singer', 'song__singer__vtuber_groups') \
        .exclude(song__singer__vtuber_groups__unit__in=exclude_group) \
        .order_by(order_query)[:rank_num_to]

    pp(records[0].song.singer)

    template = 'songs/ranker.html'
    context = {
        'records': records,
    }

    return render(request, template, context)
