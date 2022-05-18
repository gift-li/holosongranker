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
    # * var: get_records_page()
    default_page = 1
    on_each_side = 2
    on_ends = 3
    # * Others
    date_select_list = Record.get_date_list()['date'].tolist()

    # 取得搜尋條件
    order_query, date_query = get_records_search_query(request)

    # 取得資料
    records = get_records_list(date_query, order_query, order_by='DSC')

    # 分頁
    records, page_range = get_records_page(
        request, records, default_page, on_each_side, on_ends)

    template = 'songs/ranker.html'
    context = {
        'records': records,
        'date_select_list': date_select_list,
        'page_range': page_range
    }

    return render(request, template, context)


def get_records_search_query(request):
    order_query = 'weekly_view'
    date_query = Record.get_lastest_record_date()

    if request.method == 'GET':
        # * 沒快取: 設定為"周觀看"+"最新日期"
        if 'songs_view_select' not in request.session:
            request.session['songs_view_select'] = order_query
            request.session['songs_date_select'] = datetime.strftime(
                date_query, "%Y/%m/%d")

    if request.method == 'POST':
        # * 取得POST的搜尋條件
        request.session['songs_view_select'] = request.POST.get(
            'view_select')
        request.session['songs_date_select'] = request.POST.get(
            'date_select')

    # * 用Session賦值
    order_query = request.session['songs_view_select']
    date_query = datetime.strptime(
        request.session['songs_date_select'], "%Y/%m/%d").date()

    return order_query, date_query


def get_records_page(request, data, default_page=1, on_each_side=2, on_ends=3):
    page = request.GET.get('page', default_page)
    p = Paginator(data, 10)
    try:
        data = p.page(page)
    except PageNotAnInteger:
        data = p.page(default_page)
    except EmptyPage:
        data = p.page(p.num_pages)
    page_range = p.get_elided_page_range(
        page, on_each_side=on_each_side, on_ends=on_ends)

    return data, page_range


def get_records_list(date_query, order_query, order_by='DSC'):
    # * 預設日期: 最新更新日期
    if (date_query == None):
        date_query = Record.get_lastest_record_date()
    # * 順序: 正號 / 逆序: 負號
    if order_by == 'DSC':
        order_by = '-'
    else:
        order_by = ''

    try:
        records = Record.objects.filter(date=date_query) \
            .prefetch_related('song', 'song__singer', 'song__singer__vtuber_groups') \
            .order_by(str(order_by + order_query))
    except:
        records = Record.objects.filter(date=Record.get_lastest_record_date()) \
            .prefetch_related('song', 'song__singer', 'song__singer__vtuber_groups') \
            .order_by('-weekly_view')

    return records
