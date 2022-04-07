from django.contrib import admin
from .models import Song, Vtuber, Group


@admin.register(Vtuber)
class VtuberAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'publish_at']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Group._meta.fields]
    ordering = ('vtuber', 'unit')
