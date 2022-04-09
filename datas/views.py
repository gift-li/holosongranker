from django.shortcuts import render
from .models import *


def Index(request):
    # TODO: 撈資料 & 改順序
    datas = {}
    # TODO: 放入表頭標籤eg. 排名、歌曲名稱...
    table_headers = []

    return render(request, 'datas/index.html', {
        'datas': datas,
        'table_headers': table_headers
    })
