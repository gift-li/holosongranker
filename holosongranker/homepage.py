from django.shortcuts import render
from django.db.models import Sum
from datas.models import *
from pprint import pp


def Index(request):
    singer = Vtuber.objects.prefetch_related('vtuber_groups') \
        .exclude(vtuber_groups__unit__in=[Group.Unit.GROUP]) \
        .count()
    song = Song.objects.count()
    total_view = sum(Record.objects.filter(
        date=Record.get_lastest_record_date())
        .values_list('total_view', flat=True))
    over_million_song = Record.objects.filter(
        date=Record.get_lastest_record_date()) \
        .filter(total_view__gt=1000000) \
        .count()
    over_10_million_song = Record.objects.filter(
        date=Record.get_lastest_record_date()) \
        .filter(total_view__gt=10000000) \
        .count()
    total_weekly_view = sum(Record.objects.filter(
        date=Record.get_lastest_record_date())
        .values_list('weekly_view', flat=True))

    holodata = {
        'singer': singer,
        'song': song,
        'total_view': total_view,
        'over_million_song': over_million_song,
        'over_10_million_song': over_10_million_song,
        'total_weekly_view': total_weekly_view,
    }

    template = 'index.html'
    context = {
        'holodata': holodata,
    }

    return render(request, template, context)
