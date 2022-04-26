from django.shortcuts import render
from datas.models import *
from django.db.models import Prefetch, Max
from pprint import pp

# 歌手排名


def Ranker(request):
    # TODO: Vtuber
    # * 排序: 總觀看量(大->小)
    vtubers = Vtuber.objects.prefetch_related(
        'vtuber_groups')[:1]
    for v in vtubers:
        pp(list(v.sing_songs.values()))
    template = 'singers/ranker.html'
    context = {
        'vtubers': vtubers,
    }

    return render(request, template, context)

# 歌手分類選單


def Menu(request):
    template = 'singers/menu.html'

    return render(request, template)

# 選定歌手的個人介紹/資訊(by id)


def Profile(request, id):
    vtuber = Vtuber.objects.filter(pk=id).get()

    template = 'singers/profile.html'
    context = {
        'vtuber': vtuber
    }

    return render(request, template, context)
