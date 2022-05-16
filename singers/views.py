from datetime import datetime
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)
from datas.models import *
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from pprint import pp

# 歌手排名


@require_http_methods(['GET', 'POST'])
def Ranker(request):
    # * var: get_ranker_records()
    exclude_group = [Group.Unit.GROUP]
    # * var: get_records_page()
    default_page = 1
    on_each_side = 2
    on_ends = 3
    # * Others
    date_select_list = VtuberRecord.get_date_list()['date'].tolist()

    # 取得搜尋條件
    order_query, date_query = get_records_search_query(request)

    # 取得資料
    records = get_records_list(
        date_query, order_query, exclude_group, order_by='DSC')

    # 分頁
    records, page_range = get_records_page(
        request, records, default_page, on_each_side, on_ends)

    template = 'singers/ranker.html'
    context = {
        'records': records,
        'date_select_list': date_select_list,
        'page_range': page_range,
    }

    return render(request, template, context)

# 用於排行版推播


@require_http_methods(['GET', 'POST'])
def Broadcast(request):
    # search querys setting
    order_query = '-total_view_weekly_growth'
    exclude_group = [Group.Unit.GROUP]
    rank_num_to = 10
    date_query = VtuberRecord.get_lastest_record_date()
    date_select_list = VtuberRecord.get_date_list()['date'].tolist()

    if request.method == 'GET':
        request.session['singers_view_select'] = order_query
        request.session['singers_date_select'] = datetime.strftime(
            date_query, "%Y/%m/%d")

    if request.method == 'POST':
        request.session['singers_view_select'] = request.POST.get(
            'view_select')
        request.session['singers_date_select'] = request.POST.get(
            'date_select')
        order_query = str('-' + request.POST.get('view_select'))
        date_query = datetime.strptime(
            request.POST.get('date_select'), "%Y/%m/%d").date()

    # * 嘗試抓取資料，失敗使用預設抓取
    try:
        vtuber_record_list = VtuberRecord.objects.filter(
            date=date_query) \
            .prefetch_related('vtuber', 'vtuber__vtuber_groups') \
            .exclude(vtuber__vtuber_groups__unit__in=exclude_group) \
            .order_by(order_query)[:rank_num_to]
    except:
        vtuber_record_list = VtuberRecord.objects.filter(
            date=VtuberRecord.get_lastest_record_date()) \
            .prefetch_related('vtuber', 'vtuber__vtuber_groups') \
            .exclude(vtuber__vtuber_groups__unit__in=exclude_group) \
            .order_by('-total_view_weekly_growth')[:rank_num_to]

    template = 'singers/broadcast.html'
    context = {
        'vtuber_record_list': vtuber_record_list,
        'date_select_list': date_select_list,
    }

    return render(request, template, context)


# 歌手分類選單
def Menu(request):
    group_query = 'all'
    selected = group_query

    if request.method == 'POST':
        group_query = request.POST.get('group_query')
        selected = group_query

    if group_query != 'all':
        list = Vtuber.objects.prefetch_related('vtuber_groups') \
            .filter(vtuber_groups__unit__in=[group_query])
    else:
        list = Vtuber.objects.all()

    units = [unit.value for unit in Group.Unit]

    template = 'singers/menu.html'
    context = {
        'list': list,
        'units': units,
        'selected': selected,
    }
    return render(request, template, context)

# 選定歌手的個人介紹/資訊(by id)


def Profile(request, id):
    default_page = 1
    is_select_nav_song = False

    profile = VtuberRecord.objects.filter(vtuber=id) \
        .filter(date=VtuberRecord.get_lastest_record_date()) \
        .prefetch_related('vtuber', 'vtuber__vtuber_groups').get()

    total_songs = Record.objects.filter(date=Record.get_lastest_record_date()) \
        .prefetch_related('song', 'song__singer') \
        .filter(song__singer__in=[id]) \
        .order_by('-weekly_view')

    top3_songs = total_songs[:3]

    page = request.GET.get('page', default_page)
    p = Paginator(total_songs, 10)
    try:
        total_songs = p.page(page)
    except PageNotAnInteger:
        total_songs = p.page(default_page)
    except EmptyPage:
        total_songs = p.page(p.num_pages)
    page_range = p.get_elided_page_range(
        page, on_each_side=2, on_ends=3)

    if(page != 1):
        is_select_nav_song = True

    template = 'singers/profile.html'
    context = {
        'profile': profile,
        'top3_songs': top3_songs,
        'total_songs': total_songs,
        'page_range': page_range,
        'is_select_nav_song': is_select_nav_song,
    }

    return render(request, template, context)


def get_records_search_query(request):
    order_query = 'weekly_view'
    date_query = Record.get_lastest_record_date()
    pp(request.session)
    if request.method == 'GET':
        # * 沒快取: 設定為"周觀看"+"最新日期"
        if 'singers_view_select' not in request.session:
            request.session['singers_view_select'] = order_query
            request.session['singers_date_select'] = datetime.strftime(
                date_query, "%Y/%m/%d")

    if request.method == 'POST':
        # * 取得POST的搜尋條件
        request.session['singers_view_select'] = request.POST.get(
            'view_select')
        request.session['singers_date_select'] = request.POST.get(
            'date_select')

    # * 用Session賦值
    order_query = request.session['singers_view_select']
    date_query = datetime.strptime(
        request.session['singers_date_select'], "%Y/%m/%d").date()

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


def get_records_list(date_query, order_query, exclude_group, order_by='DSC'):
    # * 預設日期: 最新更新日期
    if (date_query == None):
        date_query = Record.get_lastest_record_date()
    # * 順序: 正號 / 逆序: 負號
    if order_by == 'DSC':
        order_by = '-'
    else:
        order_by = ''

    try:
        records = VtuberRecord.objects.filter(
            date=date_query) \
            .prefetch_related('vtuber', 'vtuber__vtuber_groups') \
            .exclude(vtuber__vtuber_groups__unit__in=exclude_group) \
            .order_by(order_by + order_query)
    except:
        records = VtuberRecord.objects.filter(
            date=VtuberRecord.get_lastest_record_date()) \
            .prefetch_related('vtuber', 'vtuber__vtuber_groups') \
            .exclude(vtuber__vtuber_groups__unit__in=exclude_group) \
            .order_by('-total_view_weekly_growth')

    return records
