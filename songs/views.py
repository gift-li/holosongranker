from datetime import datetime
from datas.models import *
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from pprint import pp


@require_http_methods(['GET', 'POST'])
def Ranker(request):
    rank_num_to = 10
    order_query = '-weekly_view'
    date_query = Record.get_lastest_record_date()
    date_select_list = Record.get_date_list()['date'].tolist()

    if request.method == 'GET':
        request.session['singers_view_select'] = order_query
        request.session['singers_date_select'] = datetime.strftime(
            date_query, "%Y/%m/%d")

    if request.method == 'POST':
        request.session['songs_view_select'] = request.POST.get(
            'view_select')
        request.session['songs_date_select'] = request.POST.get(
            'date_select')

        order_query = str('-' + request.POST.get('view_select'))
        date_query = datetime.strptime(
            request.POST.get('date_select'), "%Y/%m/%d").date()

    # * 嘗試抓取資料，失敗使用預設抓取
    try:
        records = Record.objects.filter(date=date_query) \
            .prefetch_related('song', 'song__singer', 'song__singer__vtuber_groups') \
            .order_by(order_query)[:rank_num_to]
    except:
        records = Record.objects.filter(date=Record.get_lastest_record_date()) \
            .prefetch_related('song', 'song__singer', 'song__singer__vtuber_groups') \
            .order_by('-weekly_view')[:rank_num_to]

    template = 'songs/ranker.html'
    context = {
        'records': records,
        'date_select_list': date_select_list,
    }

    return render(request, template, context)
