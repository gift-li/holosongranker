from django.db import models
from django.utils import timezone


class Vtuber(models.Model):
    name = models.CharField('Vtuber姓名', max_length=255,
                            unique=True, editable=True)
    youtube_id = models.CharField(
        'Youtube ID', max_length=50, unique=True, editable=True)

    # TODO: 需要新增自動抓取填寫函式
    youtube_url = models.CharField(
        'Youtube連結', max_length=255, blank=True)
    thumbnail_url = models.URLField(
        "頻道縮圖連結", max_length=255, blank=True)

    class Meta:
        db_table = "vtuber"
        ordering = ['name', 'youtube_id']
        verbose_name = 'vtuber'
        verbose_name_plural = 'vtubers'

    def __str__(self):
        return self.name


class Group(models.Model):
    class Unit(models.TextChoices):
        GEN_0 = 'Gen-0'
        GEN_1 = '1STGEN'
        GEN_2 = 'Gen-2'
        GAMERS = 'Gamers'
        GEN_3 = 'Gen-3'
        GEN_4 = 'Gen-4'
        GEN_5 = 'Gen-5'
        HOLOX = 'holoX'
        INNK = 'Innk-music'
        IN = 'Indonisia'
        EN = 'English'
        MYTH = 'Myth'
        HOPE = 'Project-hope'
        COUNCIL = 'Council'
        OG = 'Og'

    vtuber = models.ForeignKey(
        Vtuber, on_delete=models.CASCADE, related_name="groups", verbose_name="Vtuber姓名")
    unit = models.CharField("所屬身分", max_length=255, choices=Unit.choices)

    class Meta:
        db_table = "group"
        ordering = ['unit', 'vtuber']
        verbose_name = 'group'
        verbose_name_plural = 'groups'

    def __str__(self):
        return self.unit


class Song(models.Model):
    name = models.CharField("歌曲曲名", max_length=255)
    singer = models.ManyToManyField(
        Vtuber, through='Singer_Song', through_fields=('song', 'singer') ,)
    youtube_id = models.URLField(
        "影片連結", max_length=255, unique=True, editable=True)

    # TODO: 需要填寫自動抓取填寫函式
    thumbnail_url = models.URLField("縮圖連結", max_length=255, blank=True)
    youtube_url = models.URLField("縮圖連結", max_length=255, blank=True)

    publish_at = models.DateField("發行日期", default=timezone.now)
    skip = models.BooleanField("歌手排名時跳過",default=False)

    class Meta:
        db_table = "song"
        #ordering = ['-publish_at', 'name']
        verbose_name = 'song'
        verbose_name_plural = 'songs'

    def __str__(self):
        return self.name


class Singer_Song(models.Model):
    singer = models.ForeignKey(Vtuber, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.song} {self.singer} '
        
    class Meta:
        db_table = 'songs_singer_song'