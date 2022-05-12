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

class SongModelController:

    # 將本周新歌加入資料庫
    def insert_this_week_new_song(self):
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

    # 抓取本周歌曲數據
    def insert_this_week_record(self, date): 
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
                date=date)
                record.save()

            except Exception as e:
                except_video.append(video_id)
                views_col.append(0)
                print(e)
            
                print(except_video)

    # 計算周觀看數
    def caculate_weekly_view_in_record(self, date):
        records = Record.objects.filter(date = date)
        for record in records:
            has_find , previous_record = Record.get_previous_record(record)

            if(has_find):
                weekly_view = record.total_view - previous_record.total_view
                previous_date = previous_record.date
            else:
                weekly_view = record.total_view
                previous_date =  ''

            print('{} \n在 {} ~ {} 的周觀看數成長為{}'
                .format(record.song, previous_date , record.date, weekly_view))

            record.weekly_view = weekly_view
            record.save()

    # 計算本周VTuber數據
    def insert_vtuber_record(self, date):
        vtubers = Vtuber.objects.all()
        for vtuber in vtubers:
            print(vtuber, date)
            songs = Song.objects.filter(singer = vtuber).filter(song_records__date = date).values('name', 'song_records__total_view', 'song_records__weekly_view')
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
                    date = date)
                vtuber_record.save()




def test_code():
   
    # 每週要做的事情
    # 去colab 找新歌曲 https://colab.research.google.com/drive/1Ddb4O_2UH5t5ZPkUI9ISygSR3sYGQ3Jv?usp=sharing
    this_date = '2022-5-8'

    sc = SongModelController()
    # 將本周新歌加入資料庫
    sc.insert_this_week_new_song(this_date)
    # 抓取本周歌曲數據 歌曲,日期,總觀看數
    sc.insert_this_week_record(this_date)
    # 計算周觀看數
    sc.caculate_weekly_view_in_record(this_date)
    # 計算本周VTuber的歌曲數據
    sc.insert_vtuber_record(this_date)


            
        
