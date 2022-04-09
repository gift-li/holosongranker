from unicodedata import name
import datas.youtube_api as y_api
import pandas as pd
from datas.models import Vtuber, Song

def load_vtuber_csv():
    vtuber_df = pd.read_csv('./datas/vtuber.csv') 
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
    songs_df = pd.read_csv('./datas/songs.csv') 
    print(songs_df)

    i = 0
    song_temp = ""

    start = 0
    # end = 2
    end = len(songs_df)

    for i in range(start, end):

        song_name = songs_df['title'][i]

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
            song_temp = song_name

        singer_name = songs_df['singer'][i]
        singer = Vtuber.objects.filter(name = singer_name)[0]

        song.singer.add(singer)

