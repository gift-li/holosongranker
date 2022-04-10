from django.shortcuts import render
from datas.models import *


def Index(request):
    template = 'singers/index.html'
    # TODO: Vtuber
    # * 排序: 總觀看量(大->小)
    # TODO: Song
    # * 分群: Vtuber
    # * 排序: 總觀看量
    vtubers = Vtuber.objects.all()
    songs = Song.objects.all()

    table_headers = [
        '排名', '頻道縮圖 & 連結', '歌手',
    ]
    context = {
        'table_headers': table_headers,
        'vtubers': vtubers,
        'songs': songs,
    }

    return render(request, template, context)
