from calendar import week
from email import message
import re
import this
from traceback import print_tb
from unicodedata import name

from numpy import record
import datas.youtube_api as y_api
import pandas as pd
from datas.models import Group, Record, Vtuber, Song, VtuberRecord
from django_pandas.io import read_frame
from datetime import date
import datas.google_sheet_manager as google_sheet_manager
import urllib.request


# 歌曲資料備份
def backup_songs_to_google_sheet():
    # 包含所有歌手資料，歌曲會重複
    songs_all_singer_df, songs_all_singer_worksheet = google_sheet_manager.get_sheet(google_sheet_manager.songs_all_singer_sheet_id)
    songs_all_singer_df = pd.DataFrame(columns=songs_all_singer_df.columns) # 將df資料刪除(剩下欄位)
    # 包含一個歌手資料，歌曲不會重複
    songs_df, songs_worksheet = google_sheet_manager.get_sheet(google_sheet_manager.songs_sheet_id)
    songs_df = pd.DataFrame(columns=songs_df.columns) # 將df資料刪除(剩下欄位)

    songs = Song.objects.all()
    for song in songs:
        singers = song.singer.all()
        for singer in singers:
            video_data = {'title':song.name  , 'videoId': song.youtube_id, 
                            'thumbnail_url':song.thumbnail_url, 'youtube_url':song.youtube_url, 'image': '' ,
                            'publishedAt':str(song.publish_at) , 'singer':singer.name, 'Skip':song.skip} 

            songs_all_singer_df = pd.concat([songs_all_singer_df, pd.DataFrame.from_records([video_data])], ignore_index=True)
        songs_df =  pd.concat([songs_df, pd.DataFrame.from_records([video_data])], ignore_index=True)

    google_sheet_manager.clear_worksheet(songs_worksheet)
    google_sheet_manager.clear_worksheet(songs_all_singer_worksheet)

    google_sheet_manager.update_worksheet(songs_df, songs_worksheet)
    google_sheet_manager.update_worksheet(songs_all_singer_df, songs_all_singer_worksheet)

# 歌曲紀錄備份
def backup_record_to_google_sheet():
    record_df, record_worksheet = google_sheet_manager.get_sheet(google_sheet_manager.record_sheet_id)
    record_df = pd.DataFrame(columns=record_df.columns) # 將df資料刪除(剩下欄位)

    records = Record.objects.all()

    for record in records:
        data = {'videoId' : record.song.youtube_id, 'date': str(record.date), 
                'total_view' : record.total_view, 'weekly_view': record.weekly_view}

        record_df = pd.concat([record_df, pd.DataFrame.from_records([data])], ignore_index=True)

    google_sheet_manager.clear_worksheet(record_worksheet)
    google_sheet_manager.update_worksheet(record_df, record_worksheet)

# 歌手紀錄
def backup_vtuber_record_to_google_sheet():
    record_df, record_worksheet = google_sheet_manager.get_sheet(google_sheet_manager.vtuber_record_sheet_id)
    record_df = pd.DataFrame(columns=record_df.columns) # 將df資料刪除(剩下欄位)

    records = VtuberRecord.objects.all()

    for record in records:
        data = {'vtuber' : record.vtuber.name , 'vtuber_id': record.vtuber.youtube_id, 'date': str(record.date), 
                'total_view' : record.total_view, 'weekly_view': record.weekly_view, 
                'average_view' : record.average_view, 'average_weekly_view':record.average_weekly_view,
                'song_count' : record.song_count}

        record_df = pd.concat([record_df, pd.DataFrame.from_records([data])], ignore_index=True)

    google_sheet_manager.clear_worksheet(record_worksheet)
    google_sheet_manager.update_worksheet(record_df, record_worksheet)

# 備份所有資料
def backup_all():
    backup_songs_to_google_sheet()
    backup_record_to_google_sheet()
    backup_vtuber_record_to_google_sheet()


def test_code():
    a = 1

    backup_all()
