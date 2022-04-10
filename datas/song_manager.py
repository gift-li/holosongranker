from email import message
from unicodedata import name
import datas.youtube_api as y_api
import pandas as pd
from datas.models import Vtuber, Song
from django_pandas.io import read_frame

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

# 之後來是在colab 上做好了
def find_new_song():

    # Get vtuber data : 'name', 'youtube_id'
    vtubers = Vtuber.objects.all()
    vtuber_df = read_frame(vtubers, fieldnames=['name', 'youtube_id'])
    print(vtuber_df.head())
    
    # 初始參數
    publishAfter = '2022-04-02T00:00:00Z' # 從此日期開始搜尋新歌
    start = 0 # for 迴圈開始點
    end = len(vtuber_df['youtube_id'])
    # end = 1 # for 迴圈結束點

    # YouTube Data API陪額使用量
    has_use_quate = 500
    change_quate = 9000
    youtube = y_api.set_api_key(0) # 使用分帳

     # Step1:以YouTube Data API 的 Search功能，找出所有 new songs
    videoDuration = ['short','medium']
    responses = []
    expects = []

    for j in range(start, end):
        channel_id = vtuber_df['youtube_id'][j]
    
        for i in range(2):
            request = youtube.search().list(
            part="snippet",   
            q="",
            channelId = channel_id,
            publishedAfter = publishAfter,
            maxResults = 50,
            order = 'date',
            type = 'video',
            videoDuration = videoDuration[i]
            )
            try:
                response = request.execute()
                responses.append(response)
            except:
                expects.append((vtuber_df['name'][j], videoDuration[i], j))

            # API陪額使用量超過時，切換帳號
            has_use_quate += 100
            if(has_use_quate > change_quate):
                youtube = y_api.set_api_key(1) # 使用本帳
            has_use_quate = 0
    
    print('Step1的expect:')
    print(expects)

     # Step2:從responses中，找出所有的歌曲，存進search_videos_df
    columns = ['title' , 'videoId' , 'thumbnail_url', 'youtube_url', 'image', 'publishedAt', 'singer', 'owner']
    search_videos_df = pd.DataFrame(columns = columns)

    for j in range( len(responses)):
        response = responses[j]

        for i in range(len(response['items'])):
            title = response['items'][i]['snippet']['title']
            videoId = response['items'][i]['id']['videoId']
            thumbnail_url = response['items'][i]['snippet']['thumbnails']['medium']['url']
            youtube_url = y_api.get_youtube_url(videoId)
            singer = response['items'][i]['snippet']['channelTitle']
            owner = response['items'][i]['snippet']['channelTitle']
            image = ""

            publishedAt = response['items'][i]['snippet']['publishedAt']
            publishedAt = publishedAt[:publishedAt.index('T')] # 只取日期

            video_data = {'title':title , 'videoId': videoId, 'thumbnail_url':thumbnail_url, 'youtube_url':youtube_url,
                        'image': image ,'publishedAt':publishedAt, 'singer':singer, 'owner':owner} 
            search_videos_df  = search_videos_df.append(video_data, ignore_index=True)

    print(search_videos_df.head())
    search_videos_df.to_csv('./datas/search_videos.csv')

    # Step3: 從search_videos_df中，篩選出min_second～max_second時間長度的影片
    start = 0
    end = len(search_videos_df)
    columns = ['title' , 'videoId' , 'thumbnail_url', 'youtube_url', 'image', 'publishedAt', 'singer', 'owner', 'isSong']
    new_songs_df = pd.DataFrame(columns = columns)
    min_second = 80
    max_second = 400
    

    except_video= []
    for i in range(start, end): # len(song_list_df)
        video_id = search_videos_df['videoId'][i]

        try:
            request = youtube.videos().list(
                part= "snippet,statistics,contentDetails", 
                id= video_id
            )

            response = request.execute()

            duration_raw = response['items'][0]['contentDetails']['duration']
            second = y_api.get_second(duration_raw)

            # 時間在min_second與max_second之間的，在放入
            if(second < max_second):
                if(second > min_second):
                    new_songs_df = new_songs_df.append(search_videos_df.iloc[i])
        except:
            except_video.append(video_id)

    print('Step3的expect:')
    print(except_video)

    print(new_songs_df.head())
    new_songs_df.to_csv('./datas/csv/new_songs_raw.csv')


def add_new_song_to_models():
    songs_df = pd.read_csv('./datas/csv/new_songs.csv') 

    start = 0
    # end = 2
    end = len(songs_df)

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

def test():
    # songs = Song.objects.all()
    # print(songs[15].singer.all())
    # load_vtuber_csv()
    # load_songs_csv()
    # vtuber =  Vtuber.objects.filter(name ="")
    # print(vtuber)
    find_new_song()

    a = 1
