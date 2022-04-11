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
    # singer = models.ManyToManyField(
    #     Vtuber, through='Singer_Song', through_fields=('song', 'singer') ,)
    singer = models.ManyToManyField(
        Vtuber, related_name="sing_songs", verbose_name="歌手")
    youtube_id = models.URLField(
        "影片連結", max_length=255, unique=True, editable=True)

    thumbnail_url = models.URLField("縮圖連結", max_length=255, blank=True)
    youtube_url = models.URLField("縮圖連結", max_length=255, blank=True)

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
    
    total_view = models.IntegerField('總觀看數', blank=True, editable=True, default=0)
    weekly_view = models.IntegerField('周觀看數成長', blank=True, editable=True, default=0)
    

    def __str__(self):
        return self.song.name

    def get_dates():
        dates = Record.objects.values('date').distinct()
        date_df = read_frame(dates, fieldnames=['date'])

        return date_df.sort_values(['date'],ascending=False)
    
    def get_last_date(now_date):
        date_df = Record.get_dates()

        now_date_index = date_df[date_df['date'] ==  now_date].index.values

        if(len(now_date_index) == 0 ):
            print('找不到{}'.format(now_date))
            return False, now_date
        
        if(now_date_index[0] == 0):
            print('找不到上週資料')
            return False, now_date
        
        last_date = date_df['date'][now_date_index[0]-1]

        return True, last_date