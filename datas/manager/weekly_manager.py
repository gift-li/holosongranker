

import datas.manager.backup_manager as backup_manager
from datas.manager.song_manager import SongModelController, GraphDataCreater
from datas.manager.image_download_manager import ImageDownloader
from datas.models import Group, Record, Vtuber, Song, VtuberRecord


# 每週要做的事情
def weekly_work():
    
    # 先將setting 設為的 DEBUG = True(32)

    # 1.去colab 找新歌曲 https://colab.research.google.com/drive/1Ddb4O_2UH5t5ZPkUI9ISygSR3sYGQ3Jv?usp=sharing
    this_date = '2022-11-06'

    
    # python manage.py test datas
    # 2.更新歌曲資料進資料庫
    sc = SongModelController()
    # # 將本周新歌加入資料庫
    # sc.insert_this_week_new_song()
    # 抓取本周歌曲數據 歌曲,日期,總觀看數
    sc.insert_this_week_record(this_date)
    # 計算周觀看數
    sc.caculate_weekly_view_in_record(this_date)
    # 計算本周VTuber的歌曲數據
    sc.insert_vtuber_record(this_date)


    # # 2.5. 更新VT頭像、頻道縮圖
    # imgdownloader = ImageDownloader()
    # # 抓取Vtuber頻道縮圖、封面
    # imgdownloader.download_vtuber_image()
    # # 抓取歌曲縮圖
    # imgdownloader.download_songs_image()

    # 3.取的比賽圖所需歌曲資料
    # # 連結: https://hackmd.io/@Cobra3279/S1qr2Rnb5/%2F5kM-oz_STe22hhlu2YUzvQ
    # gc = GraphDataCreater()
    # dates = Record.get_date_list()['date'][:5].tolist()[::-1]
    # print(dates)

    # # 歌曲比賽圖
    # gc.get_songs_for_bar_chart(dates)
    # gc.get_songs_for_line_chart(dates)

    # # 歌手比賽圖
    # gc.get_vtubers_for_bar_chart(dates)
    # gc.get_vtubers_for_line_chart(dates)

    # # # 4. 備份資料
    # backup_manager.backup_all()
    
    
    # 5.輸出sql檔案
    ## https://hackmd.io/@Cobra3279/S1qr2Rnb5/%2FjLpyCY0YReOe9ddjFgsaJg

    # ˊ6. 將setting 設為的 DEBUG = False

    # 2. 每月
    # # 1.抓取Top1連結
    # gc = GraphDataCreater()
    # dates = Record.get_date_list()['date'][:5].tolist()[::-1]
    # print(dates)
    # gc.get_top1_songs(dates)


    # # 2. 抓取月觀看數資料
    # gc = GraphDataCreater()
    # dates = Record.get_date_list()['date'][:5].tolist()[::-1]
    # print(dates)
    # gc.get_songs_sum(dates)
    # gc.get_vtubers_sum(dates)

    # gc.get_vtubers_for_bar_chart(dates)
    # gc.get_vtubers_for_line_chart(dates)
    

