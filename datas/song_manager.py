from calendar import week
from email import message
import this
from traceback import print_tb
from unicodedata import name
import datas.youtube_api as y_api
import pandas as pd
from datas.models import Group, Record, Vtuber, Song, VtuberRecord
from django_pandas.io import read_frame
from datetime import date
import datas.google_sheet_manager as google_sheet_manager
import datas.backup_manager as backup_manager
import urllib.request

##### Songs #####

def add_this_week_new_song_to_models():
    # new_songs_df = pd.read_csv('./datas/csv/new_songs.csv') 
    new_songs_df , new_songs_worksheet = google_sheet_manager.get_sheet(google_sheet_manager.new_songs_sheet_id)

    start = 0
    # end = 2
    end = len(new_songs_df)
    song_temp = ''

    # 縮圖路徑
    thumbnails_path = 'static/img/song_thumbnails/'

    for i in range(start, end):

        song_name = new_songs_df['title'][i]
        singer_name = new_songs_df['singer'][i]
        singer = Vtuber.objects.filter(name = singer_name)[0]

        # 是否為一首歌多個歌手
        if(song_name != song_temp):
            # 判斷是否已經有此資料
            find_song = len(Song.objects.filter(name = song_name))
            if(find_song >0):
                message = '已經有：' + song_name
                print(message)

                
            else:
                skip = False
                if(new_songs_df['Skip'][i] == 'TRUE'):
                    skip = True

                song = Song(name = song_name, 
                    youtube_id= new_songs_df['videoId'][i], 
                    thumbnail_url= new_songs_df['thumbnail_url'][i],
                    youtube_url = new_songs_df['youtube_url'][i],
                    publish_at = new_songs_df['publishedAt'][i],
                    skip = skip)
                song.save()
                song.singer.add(singer)
                song_temp = song_name

                # 下載影片縮圖
                url = new_songs_df['thumbnail_url'][i].replace("mqde", "sdde")
                thumbnails_file_name = thumbnails_path + new_songs_df['youtube_url'][i]  + '.png'
                try:
                    urllib.request.urlretrieve(url, thumbnails_file_name)
                except:
                    print(url)

        else:
            song.singer.add(singer)

##### Record ######

def add_this_week_record_to_models(this_date): 
    youtube = y_api.set_api_key(2) # 使用分帳
    songs = Song.objects.all()
    except_video = []
    views_col = []
    start = 0
    end = len(songs)
    # end = 5
    for i in range(start, end):
        video_id = songs[i].youtube_id

        try:
            request = youtube.videos().list(
            part= "snippet,statistics", 
            id= video_id
            )
            response = request.execute()
            viewCount = response['items'][0]['statistics']['viewCount']
            views_col.append(viewCount)

            record = Record(song = songs[i], 
            total_view = viewCount, 
            date=this_date)
            record.save()

        except Exception as e:
            except_video.append(video_id)
            views_col.append(0)
            print(e)
        
            print(except_video)
    
def add_weekly_view_to_record_by_this_date(this_date):
    records = Record.objects.filter(date = this_date)

    for record in records:
        add_weekly_view_to_record(record)

def add_weekly_view_to_record(now_record):
    has_find , previous_record = Record.get_previous_record(now_record)

    if(has_find):
        weekly_view = now_record.total_view - previous_record.total_view
        previous_date = previous_record.date
    else:
        weekly_view = now_record.total_view
        previous_date =  ''

    print('{} \n在 {} ~ {} 的周觀看數成長為{}'
        .format(now_record.song, previous_date , now_record.date, weekly_view))

    now_record.weekly_view = weekly_view
    now_record.save()

##### Vtuber Record #########

def add_vtuber_record_by_date(now_date):
    vtubers = Vtuber.objects.all()
    for vtuber in vtubers:
        print(vtuber, now_date)
        songs = Song.objects.filter(singer = vtuber).filter(song_records__date = now_date).values('name', 'song_records__total_view', 'song_records__weekly_view')
        df = read_frame(songs)
        if(len(df) != 0):
            total_view_df = df[df['song_records__total_view'] != 0] # 篩掉觀看數為0
            total_view = total_view_df['song_records__total_view'].sum()
            song_count = len(total_view_df)
            average_view  = int(total_view/ song_count)

            weekly_view_df = df[df['song_records__weekly_view'] != 0] # 篩掉觀看數為0
            total_view_weekly_growth = weekly_view_df['song_records__weekly_view'].sum()
            weekly_song_count = len(weekly_view_df)
            average_view_weekly_growth = int(total_view_weekly_growth /weekly_song_count)

            vtuber_record = VtuberRecord(
                vtuber = vtuber,
                total_view = total_view,
                total_view_weekly_growth = total_view_weekly_growth,
                average_view = average_view,
                average_view_weekly_growth = average_view_weekly_growth,
                song_count = song_count,
                date = now_date)
            vtuber_record.save()
            
  
def test_code():
    a = 1
   
    # 每週要做的事情
    # 去colab 找新歌曲 https://colab.research.google.com/drive/1Ddb4O_2UH5t5ZPkUI9ISygSR3sYGQ3Jv?usp=sharing
    this_date = '2022-5-8'
    # add_this_week_new_song_to_models() # 新增新歌到songs
    # add_this_week_record_to_models(this_date) # 新增本周所有歌曲的record
    # add_weekly_view_to_record_by_this_date(this_date) # 計算本周歌曲的 weekly record
    
    # add_vtuber_record_by_date(this_date)

    # backup_manager.backup_all() # 備份資料至google sheet

    # records = VtuberRecord.objects.filter(date = '2022-03-09')
    # print(records)
    # records.delete()



            
        
