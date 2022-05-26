from django.contrib import admin
from .models import *


@admin.register(Vtuber)
class VtuberAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'publish_at', 'skip')
    ordering = ('-publish_at',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Group._meta.fields]
    ordering = ('vtuber', 'unit')


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Record._meta.fields]
    ordering = ('date', 'song')

@admin.register(VtuberRecord)
class VtuberRecordAdmin(admin.ModelAdmin):
    list_display = [field.name for field in VtuberRecord._meta.fields]
    ordering = ('vtuber', 'date')
    list_filter = ('vtuber', 'date')