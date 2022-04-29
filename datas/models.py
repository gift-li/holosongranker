from django.db import models
from django.utils import timezone
from django_pandas.io import read_frame


class Vtuber(models.Model):
    name = models.CharField('Vtuber姓名', max_length=255,
                            unique=True, editable=True)
    youtube_id = models.CharField(
        'Youtube ID', max_length=50, unique=True, editable=True)

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
        IN = 'Indonisia'
        EN = 'English'
        MYTH = 'Myth'
        HOPE = 'Project-hope'
        COUNCIL = 'Council'
        GROUP = 'Group'

    vtuber = models.ForeignKey(
        Vtuber, on_delete=models.CASCADE, related_name="vtuber_groups", verbose_name="Vtuber姓名")
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
    # singer = models.ManyToManyField(
    #     Vtuber, through='Singer_Song', through_fields=('song', 'singer') ,)
    singer = models.ManyToManyField(
        Vtuber, related_name="sing_songs", verbose_name="歌手")
    youtube_id = models.CharField(
        "影片ID", max_length=255, unique=True, editable=True)

    thumbnail_url = models.URLField("縮圖連結", max_length=255, blank=True)
    youtube_url = models.URLField("影片連結", max_length=255, blank=True)

    publish_at = models.DateField("發行日期", default=timezone.now)
    skip = models.BooleanField("歌手排名時跳過", default=False)

    class Meta:
        db_table = "song"
        ordering = ['name', '-publish_at']
        verbose_name = 'song'
        verbose_name_plural = 'songs'

    def __str__(self):
        return self.name


class Record(models.Model):
    song = models.ForeignKey(
        Song, on_delete=models.CASCADE, related_name="song_records", verbose_name="歌曲")
    date = models.DateField("資料取得日期", default=timezone.now)

    total_view = models.IntegerField(
        '總觀看數', blank=True, editable=True, default=0)
    weekly_view = models.IntegerField(
        '周觀看數成長', blank=True, editable=True, default=0)

    def __str__(self):
        return self.song.name

    # 取得歌曲最新紀錄日期
    def get_lastest_record_date():
        return Record.objects.values_list('date', flat=True).latest('date')

    def get_date_list():
        dates = Record.objects.values('date').distinct()
        date_df = read_frame(dates, fieldnames=['date'])

        return date_df.sort_values(['date'], ascending=False).reset_index()

    # 取得上一筆紀錄的日期
    def get_last_date(now_date):
        last_date = Record.objects.filter(date__lt=now_date).values(
            'date').distinct().order_by('-date').first()

        if(last_date != None):
            last_date = last_date['date']

        return last_date != None, last_date

    # 取得前一筆紀錄
    def get_previous_record(now_record):
        previous_record = Record.objects.filter(date__lt=now_record.date).filter(
            song=now_record.song).order_by('-date').first()

        return previous_record != None, previous_record


class VtuberRecord(models.Model):
    vtuber = models.ForeignKey(
        Vtuber, on_delete=models.CASCADE, related_name="vtuber_record", verbose_name="Vtuber姓名")
    total_view = models.IntegerField(
        '總觀看數', blank=True, editable=True, default=0)
    total_view_weekly_growth = models.IntegerField(
        '周總觀看數成長', blank=True, editable=True, default=0)
    average_view = models.IntegerField(
        '平均觀看數', blank=True, editable=True, default=0)
    average_view_weekly_growth = models.IntegerField(
        '平均觀看數週成長', blank=True, editable=True, default=0)

    song_count = models.IntegerField(
        '歌曲數量', blank=True, editable=True, default=0)

    date = models.DateField("資料取得日期", default=timezone.now)

    def __str__(self):
        return self.vtuber.name
