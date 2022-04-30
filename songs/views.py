from django.shortcuts import render
from datas.models import *
from django.db.models import Max
from pprint import pp


def Ranker(request):
    order_query = str('-total_view')
    rank_num_to = 5

    records = Record.objects.filter(date=Record.get_lastest_record_date()) \
        .prefetch_related('song', 'song__singer', 'song__singer__vtuber_groups') \
        .order_by(order_query)[:rank_num_to]

    template = 'songs/ranker.html'
    context = {
        'records': records,
    }

    return render(request, template, context)
