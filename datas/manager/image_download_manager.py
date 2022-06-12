
from traceback import print_tb
from unicodedata import name


import datas.manager.youtube_api as y_api
import pandas as pd
from datas.models import  Song, Vtuber
import datas.manager.google_sheet_manager as google_sheet_manager
import urllib.request


# 抓取圖片方法
class ImageDownloader:
    # 抓取Vtuber頻道縮圖、封面
    def download_vtuber_image(self):
        youtube = y_api.set_api_key(2) # 使用分帳

        # vtuber_df = pd.read_csv('./datas/csv/vtuber.csv') 
        vtuber_df , vtuber_worksheet = google_sheet_manager.get_sheet(google_sheet_manager.group_sheet_id)
        thumbnails_path = 'static/img/vtuber_thumbnails/'
        banners_path = 'static/img/vtuber_banners/'

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

            # 更新資料庫縮圖連結
            vtuber = Vtuber.objects.filter(youtube_id = channel_id)[0]
            vtuber.thumbnail_url = thumbnails_url
            vtuber.save()
            # 頻道封面
            try:
                banners_url = response['items'][0]['brandingSettings']['image']['bannerExternalUrl']
                
                index = banners_url.rindex('/') # 從Claude_Monet_1.jpg中，找到最右邊"_"的位置 
                banners_id = banners_url[index:]
                banners_yt3_url = 'https://yt3.ggpht.com/' + banners_id + '=w2560-fcrop64=1,00005a57ffffa5a8-k-c0xffffffff-no-nd-rj'

                banners_file_name = banners_path + channel_id + '.png'
                # print(banners_yt3_url)
                urllib.request.urlretrieve(banners_yt3_url, banners_file_name)


            except:
                print('No Banner: ' + vtuber_df['Chanel Name'][i])
            
    # 抓取Vtuber歌曲縮圖
    def download_songs_image(self):
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

    def download_song_image(self, id):
        url =  'https://i.ytimg.com/vi/' + id  + '/sddefault.jpg'
        thumbnails_path = 'static/img/song_thumbnails/'
        thumbnails_file_name = thumbnails_path + id  + '.png'
        try:
            urllib.request.urlretrieve(url, thumbnails_file_name)
        except:
            print('{}縮圖下載失敗'.format(url))
