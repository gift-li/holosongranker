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

