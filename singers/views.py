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
    # search querys setting
    order_query = '-total_view_weekly_growth'
    exclude_group = [Group.Unit.GROUP]
    rank_num_to = 10
    date_query = VtuberRecord.get_lastest_record_date()
    date_select_list = VtuberRecord.get_date_list()['date'].tolist()
    message = ''

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

    message = getSearchMessage(order_query, date_query)

    template = 'singers/ranker.html'
    context = {
        'vtuber_record_list': vtuber_record_list,
        'date_select_list': date_select_list,
        'message': message,
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
    profile = VtuberRecord.objects.filter(vtuber=id) \
        .filter(date=VtuberRecord.get_lastest_record_date()) \
        .prefetch_related('vtuber', 'vtuber__vtuber_groups').get()

    total_songs = Record.objects.filter(date=Record.get_lastest_record_date()) \
        .prefetch_related('song', 'song__singer') \
        .filter(song__singer__in=[id]) \
        .order_by('-weekly_view')

    top3_songs = total_songs[:3]

    template = 'singers/profile.html'
    context = {
        'profile': profile,
        'top3_songs': top3_songs,
        'total_songs': total_songs,
    }

    return render(request, template, context)

# 搜尋條件文字訊息生成


def getSearchMessage(order_query, date_query):
    message = ''
    return message
