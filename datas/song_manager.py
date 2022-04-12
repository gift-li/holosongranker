from calendar import week
from email import message
import this
from traceback import print_tb
from unicodedata import name
import datas.youtube_api as y_api
import pandas as pd
from datas.models import Record, Vtuber, Song
from django_pandas.io import read_frame
from datetime import date


##### Vtuber #####

def load_vtuber_csv():
    vtuber_df = pd.read_csv('./datas/csv/vtuber.csv') 
    print(vtuber_df)

    start = 0
    end = len(vtuber_df)

    for i in range(start, end):
        youtube_id = vtuber_df['channel_id'][i]
        youtube_url = 'https://www.youtube.com/channel/' + youtube_id

        vtuber = Vtuber(name = vtuber_df['Chanel Name'][i], 
            youtube_id = youtube_id, 
            youtube_url=youtube_url, 
            thumbnail_url=vtuber_df['img_url'][i])
        vtuber.save()


##### Songs #####

def load_songs_csv():
    songs_df = pd.read_csv('./datas/csv/songs.csv') 
    print(songs_df)

    i = 0
    song_temp = ""

    start = 0
    # end = 2
    end = len(songs_df)

    for i in range(start, end):

        song_name = songs_df['title'][i]
        singer_name = songs_df['singer'][i]
        singer = Vtuber.objects.filter(name = singer_name)[0]

        if(song_name != song_temp):
            skip = False
            if(songs_df['Skip'][i] == 'TRUE'):
                skip = True

            song = Song(name = song_name, 
                youtube_id= songs_df['videoId'][i], 
                thumbnail_url= songs_df['thumbnail_url'][i],
                youtube_url = songs_df['youtube_url'][i],
                publish_at = songs_df['publishedAt'][i],
                skip = skip)
            song.save()
            # song.singer.add(singer)
            song_temp = song_name
        # else:
        song.singer.add(singer)

def add_new_songs_to_models():
    # 記得要上傳new_songs.csv
    songs_df = pd.read_csv('./datas/csv/new_songs.csv') 

    start = 0
    # end = 2
    end = len(songs_df)
    song_temp = ''

    for i in range(start, end):

        song_name = songs_df['title'][i]
        singer_name = songs_df['singer'][i]
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
                if(songs_df['Skip'][i] == 'TRUE'):
                    skip = True

                song = Song(name = song_name, 
                    youtube_id= songs_df['videoId'][i], 
                    thumbnail_url= songs_df['thumbnail_url'][i],
                    youtube_url = songs_df['youtube_url'][i],
                    publish_at = songs_df['publishedAt'][i],
                    skip = skip)
                song.save()
                song.singer.add(singer)
                song_temp = song_name
        else:
            song.singer.add(singer)

##### Record ######

def load_record_csv():
    record_df = pd.read_csv('./datas/csv/record.csv') 
    print(record_df)

    start = 0
    end = len(record_df)

    for i in range(start, end):
        youtube_id = record_df['videoId'][i]
        song = Song.objects.filter(youtube_id = youtube_id)[0]

        view = record_df['view'][i]
        date = record_df['date'][i]

        record = Record(song = song, 
            total_view = view,
            weekly_view = 0, 
            date=date)
        record.save()

    add_all_weekly_view_to_record()

def update_weekly_song_record():
    last_date = '2022-4-3'
    this_date = '2022-4-10'
    youtube = y_api.set_api_key(1) # 使用分帳

    songs = Song.objects.all()
    except_video = []
    views_col = []
    start = 0
    end = len(songs)
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
            view = viewCount, 
            date=date)
            record.save()

        except:
            except_video.append(video_id)
            views_col.append(0)
        
        print(except_video)

def add_all_weekly_view_to_record():
    records = Record.objects.all()

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


def test():
    a = 1
    # songs = Song.objects.all()
    # print(songs[15].singer.all())
    # load_vtuber_csv()
    # load_songs_csv()
    # vtuber =  Vtuber.objects.filter(name ="")
    # print(vtuber)
    # add_new_songs_to_models()
    
    # update_weekly_song_record()
    # songs = Song.objects.all()[0].test()
    # songs = Song.objects.select_related('sing_songs')
    # print(songs.query)

    # dates = Record.objects.values('date').distinct()
    # date_df = read_frame(dates, fieldnames=['date'])
    # date_df = date_df.sort_values(['date'],ascending=False)
    # print(date_df)

    # record = Record.objects.all()[2000]
    # last_record = Record.get_last_record(record)
    # print(last_record)
    # add_weekly_view(record)

    add_all_weekly_view_to_record()

    # Record.objects.all().delete()
    # load_record_csv()

    # dates = Record.get_dates()
    # now_date = dates[0]

    # print(now_date)
    # last_date = Record.objects.filter(date__lt  = now_date['date']).values('date').distinct().order_by('-date').first()
    # # .distinct('date').order_by('date')

    # print(last_date)

    # now_date = Record.objects.all()[1000].date

    # last_date = Record.objects.filter(date__lt  = now_date).values('date').distinct().order_by('-date').first()['date']
    # print(last_date)

    # print(records)
    

            
        
