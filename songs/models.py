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
        db_table = "hololive"
        ordering = ['unit', 'vtuber']

    def __str__(self):
        return self.unit


class Song(models.Model):
    name = models.CharField("歌曲曲名", max_length=255)
    owner = models.ForeignKey(
        Vtuber, on_delete=models.CASCADE, related_name="own_songs", verbose_name="影片持有人")
    singer = models.ManyToManyField(
        Vtuber, related_name="sing_songs", verbose_name="歌手")
    youtube_id = models.URLField(
        "影片連結", max_length=255, unique=True, editable=True)

    # TODO: 需要填寫自動抓取填寫函式
    thumbnail_url = models.URLField("縮圖連結", max_length=255, blank=True)
    youtube_url = models.URLField("縮圖連結", max_length=255, blank=True)

    publish_at = models.DateField("發行日期", default=timezone.now)

    class Meta:
        db_table = "song"
        ordering = ['-publish_at', 'name', 'owner']

    def __str__(self):
        return self.name
