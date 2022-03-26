from django.contrib import admin
from .models import Song, Vtuber, Group


class VtuberAdmin(admin.ModelAdmin):
    list_display = ['name']


class SongAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'publish_at']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['vtuber', 'unit']


admin.site.register(Vtuber, VtuberAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Group, GroupAdmin)
