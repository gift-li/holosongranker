from django.shortcuts import render
from datas.models import *
# Create your views here.


def Index(request):
    # TODO: 撈資料 & 改順序
    datas = {}
    # TODO: 放入表頭標籤eg. 排名、歌曲名稱...
    table_headers = []

    return render(request, 'singers/index.html', {
        'datas': datas,
        'table_headers': table_headers
    })
