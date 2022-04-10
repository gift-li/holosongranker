# 建立分析器，連結到Google Cloud Platform
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def set_api_key(index):
  DEVELOPER_KEY = 'AIzaSyCNUQ5A1BcgQjv2r6X2G93tovFzdf18oUo' # 你的金鑰
  DEVELOPER_KEY2 = 'AIzaSyC5Ejf4LJzcbsQ2Krx273E4dWNy_NjdJn0' # 分帳的金鑰
  keys = [DEVELOPER_KEY, DEVELOPER_KEY2]
  youtube = build('youtube', 'v3', developerKey=keys[index])
  return youtube

def get_youtube_url(id):
  return 'https://www.youtube.com/watch?v=' + id

def get_second(duration_raw):
  duration = duration_raw[2:]
  m_index = duration.find('M')
  s_index = duration.find('S')
  h_index = duration.find('H')

  if (h_index == -1) : 
    hour = 0
  else:
    hour = int(duration[:h_index])
    

  if (m_index == -1) :
    minute = 0
  else:
    minute = int(duration[h_index + 1 :m_index])


  if (s_index == -1) :
    second = 0
  else:
    second = int(duration[m_index + 1:s_index])

  total_second = 3600 * hour + 60 * minute + second
  return total_second 