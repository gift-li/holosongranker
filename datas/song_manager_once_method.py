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
import urllib.request

########## 一次性方法 #################

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

def load_group_sheet():
    group_df, group_df_worksheet = google_sheet_manager.get_sheet(google_sheet_manager.group_sheet_id )

    start = 0
    # end = 2
    end = len(group_df)

    for i in range(start, end):

        vtuber_str = group_df['Chanel Name'][i]
        group_str = group_df['Group'][i]
        vtuber = Vtuber.objects.filter(name = vtuber_str)[0]
        print(group_str)
        unit = Group.Unit(group_str)

        group = Group(vtuber = vtuber, unit = unit)
        group.save()
        

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


##### Vtuber Record #########

def add_init_vtuber_record():
    vtubers = Vtuber.objects.all()
    date_list = Record.get_date_list()

    for vtuber in vtubers:
        for now_date in date_list['date']:
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
                
                print(vtuber_record)




##### Image #####

def download_vtuber_img_to_media():
    youtube = y_api.set_api_key(2) # 使用分帳

    vtuber_df = pd.read_csv('./datas/csv/vtuber.csv') 
    thumbnails_path = 'img/vtuber_thumbnails/'
    banners_path = 'img/vtuber_banners/'

    start = 0
    # end = 1
    end = len(vtuber_df)

    for i in range(start, end):
        channel_id = vtuber_df['channel_id'][i]
        request = youtube.channels().list(
            part= "snippet,statistics,brandingSettings",   
            id= channel_id
        )
        response = request.execute()

        # # 頻道縮圖
        thumbnails_url = response['items'][0]['snippet']['thumbnails']['medium']['url']
        thumbnails_file_name = thumbnails_path + channel_id + '.png'
        urllib.request.urlretrieve(thumbnails_url, thumbnails_file_name)

        # 頻道封面
        try:
            banners_url = response['items'][0]['brandingSettings']['image']['bannerExternalUrl']
            
            index = banners_url.rindex('/') # 從Claude_Monet_1.jpg中，找到最右邊"_"的位置 
            banners_id = banners_url[index:]
            banners_yt3_url = 'https://yt3.ggpht.com/' + banners_id + '=w2560-fcrop64=1,00005a57ffffa5a8-k-c0xffffffff-no-nd-rj'

            banners_file_name = banners_path + channel_id + '.png'
            print(banners_yt3_url)
            urllib.request.urlretrieve(banners_yt3_url, banners_file_name)
        except:
            print('No Banner: ' + vtuber_df['Chanel Name'][i])
        

def download_songs_img_to_media():
    thumbnails_path = 'static/img/song_thumbnails/'
    songs = Song.objects.all()
    except_ids = []

    for song in songs:
        youtube_id = song.youtube_id 
        url = song.thumbnail_url 
        url = url.replace("mqde", "sdde")
        # 'sdde'
        thumbnails_file_name = thumbnails_path + youtube_id  + '.png'
        print(url)
        try:
            urllib.request.urlretrieve(url, thumbnails_file_name)
        except:
            except_ids.append(url)
            print(url)

    print(except_ids)


def test_code():
    a = 1
   
    # 每週要做的事情
    this_date = '2022-4-24'

    except_ids = ['NtRpDpfE69Y','mEs80XOSSHQ','UBSx4qqeikY','ibXRzMUUWPE']
    id = except_ids[0]

    for id in except_ids:

        songs = Song.objects.filter( youtube_id = id)
        print(songs)
        record = Record.objects.filter(song = songs[0])

        print(record)
        record.delete()
        songs.delete()

    # download_songs_img_to_media()


    # add_this_week_new_song_to_models() # 新增新歌到songs
    # add_this_week_record_to_models(this_date) # 新增本周所有歌曲的record
    # add_weekly_view_to_record_by_this_date(this_date) # 計算本周歌曲的 weekly record
    
    

    

    
