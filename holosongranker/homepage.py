from django.shortcuts import render
from django.db.models import Sum
from datas.models import *
from pprint import pp

def About(request):
    template = 'about.html'

    return render(request, template)

def Index(request):
    holodata, holodata_record_date = getHolodata()
    songrank, song_record_date = getSongRank()
    singerrank, singer_record_date = getSingerRank()

    record_date = {
        'holodata': holodata_record_date,
        'song': song_record_date,
        'singer': singer_record_date,
    }

    template = 'index.html'
    context = {
        'holodata': holodata,
        'songrank': songrank,
        'singerrank': singerrank,
        'record_date': record_date,
    }

    return render(request, template, context)


def getHolodata():
    holodata_record_date = Record.get_lastest_record_date()

    singer = Vtuber.objects.prefetch_related('vtuber_groups') \
        .exclude(vtuber_groups__unit__in=[Group.Unit.GROUP]) \
        .count()

    song = Song.objects.count()

    total_view = sum(
        Record.objects.filter(date=holodata_record_date)
        .values_list('total_view', flat=True)
    )

    over_million_song = Record.objects.filter(date=holodata_record_date) \
        .filter(total_view__gt=1000000) \
        .count()

    over_10_million_song = Record.objects.filter(date=holodata_record_date) \
        .filter(total_view__gt=10000000) \
        .count()

    total_weekly_view = sum(
        Record.objects.filter(date=holodata_record_date)
        .values_list('weekly_view', flat=True)
    )

    holodata = {
        'singer': singer,
        'song': song,
        'total_view': total_view,
        'over_million_song': over_million_song,
        'over_10_million_song': over_10_million_song,
        'total_weekly_view': total_weekly_view,
    }

    return holodata, holodata_record_date


def getSongRank():
    song_record_date = Record.get_lastest_record_date()

    songs = Record.objects.filter(date=song_record_date) \
        .prefetch_related('song') \
        .order_by('-weekly_view')[:6]

    return songs, song_record_date


def getSingerRank():
    singer_record_date = VtuberRecord.get_lastest_record_date()

    singers = VtuberRecord.objects.filter(date=singer_record_date) \
        .prefetch_related('vtuber') \
        .order_by('-total_view_weekly_growth')[:10]

    return singers, singer_record_date
