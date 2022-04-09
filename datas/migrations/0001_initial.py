# Generated by Django 4.0.3 on 2022-04-09 15:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vtuber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Vtuber姓名')),
                ('youtube_id', models.CharField(max_length=50, unique=True, verbose_name='Youtube ID')),
                ('youtube_url', models.CharField(blank=True, max_length=255, verbose_name='Youtube連結')),
                ('thumbnail_url', models.URLField(blank=True, max_length=255, verbose_name='頻道縮圖連結')),
            ],
            options={
                'verbose_name': 'vtuber',
                'verbose_name_plural': 'vtubers',
                'db_table': 'vtuber',
                'ordering': ['name', 'youtube_id'],
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='歌曲曲名')),
                ('youtube_id', models.URLField(max_length=255, unique=True, verbose_name='影片連結')),
                ('thumbnail_url', models.URLField(blank=True, max_length=255, verbose_name='縮圖連結')),
                ('youtube_url', models.URLField(blank=True, max_length=255, verbose_name='縮圖連結')),
                ('publish_at', models.DateField(default=django.utils.timezone.now, verbose_name='發行日期')),
                ('skip', models.BooleanField(default=False, verbose_name='歌手排名時跳過')),
                ('singer', models.ManyToManyField(related_name='sing_songs', to='datas.vtuber', verbose_name='歌手')),
            ],
            options={
                'verbose_name': 'song',
                'verbose_name_plural': 'songs',
                'db_table': 'song',
            },
        ),
        migrations.CreateModel(
            name='Singer_Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('singer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datas.vtuber')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datas.song')),
            ],
            options={
                'db_table': 'songs_singer_song',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(choices=[('Gen-0', 'Gen 0'), ('1STGEN', 'Gen 1'), ('Gen-2', 'Gen 2'), ('Gamers', 'Gamers'), ('Gen-3', 'Gen 3'), ('Gen-4', 'Gen 4'), ('Gen-5', 'Gen 5'), ('holoX', 'Holox'), ('Innk-music', 'Innk'), ('Indonisia', 'In'), ('English', 'En'), ('Myth', 'Myth'), ('Project-hope', 'Hope'), ('Council', 'Council'), ('Og', 'Og')], max_length=255, verbose_name='所屬身分')),
                ('vtuber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='datas.vtuber', verbose_name='Vtuber姓名')),
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
                'db_table': 'group',
                'ordering': ['unit', 'vtuber'],
            },
        ),
    ]
