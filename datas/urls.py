from django.urls import path
from . import views  # 引用這個資料夾中的views檔案
from .models import *

app_name = 'datas'

urlpatterns = [
    path("", views.Index, name="index"),
]
