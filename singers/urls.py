from django.urls import path
from . import views
from datas.models import *

app_name = 'singers'

urlpatterns = [
    path("ranker/", views.Ranker, name="ranker"),
    path("profile/menu", views.Menu, name="menu"),
    path("profile/<int:id>", views.Profile, name="profile"),
]
