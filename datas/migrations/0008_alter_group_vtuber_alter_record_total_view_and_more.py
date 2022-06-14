# Generated by Django 4.0.3 on 2022-06-14 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datas', '0007_auto_20220519_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='vtuber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vtuber_groups', to='datas.vtuber', verbose_name='Vtuber姓名'),
        ),
        migrations.AlterField(
            model_name='record',
            name='total_view',
            field=models.IntegerField(blank=True, default=0, verbose_name='累積觀看數'),
        ),
        migrations.AlterField(
            model_name='record',
            name='weekly_view',
            field=models.IntegerField(blank=True, default=0, verbose_name='周觀看數'),
        ),
        migrations.AlterField(
            model_name='vtuberrecord',
            name='average_weekly_view',
            field=models.IntegerField(blank=True, default=0, verbose_name='平均周觀看數'),
        ),
        migrations.AlterField(
            model_name='vtuberrecord',
            name='total_view',
            field=models.IntegerField(blank=True, default=0, verbose_name='累積觀看數'),
        ),
        migrations.AlterField(
            model_name='vtuberrecord',
            name='weekly_view',
            field=models.IntegerField(blank=True, default=0, verbose_name='周觀看數'),
        ),
    ]
