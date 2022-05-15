from datetime import datetime
from datas.models import *
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)
from pprint import pp


@require_http_methods(['GET', 'POST'])
def Ranker(request):
    default_page = 1
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
            .order_by(order_query)
    except:
        records = Record.objects.filter(date=Record.get_lastest_record_date()) \
            .prefetch_related('song', 'song__singer', 'song__singer__vtuber_groups') \
            .order_by('-weekly_view')

    page = request.GET.get('page', default_page)
    p = Paginator(records, 10)
    try:
        records = p.page(page)
    except PageNotAnInteger:
        records = p.page(default_page)
    except EmptyPage:
        records = p.page(p.num_pages)
    page_range = p.get_elided_page_range(
        page, on_each_side=2, on_ends=3)

    template = 'songs/ranker.html'
    context = {
        'records': records,
        'date_select_list': date_select_list,
        'page_range': page_range
    }

    return render(request, template, context)
