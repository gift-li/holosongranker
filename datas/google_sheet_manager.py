import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials 

auth_json_path = './datas/google_sheet_key.json' #由剛剛建立出的憑證，放置相同目錄以供引入
gss_scopes = ['https://spreadsheets.google.com/feeds'] #我們想要取用的範圍
 #從剛剛建立的sheet，把網址中 https://docs.google.com/spreadsheets/d/〔key〕/edit 的 〔key〕的值代入 
spreadsheet_key_path = '1rq6RE8WhQXZq7UzRr1pCLQWEqoVADYDKxe3tews8S10'

songs_sheet_id = 2097225833
songs_all_singer_sheet_id = 1564903369
record_sheet_id = 2121622859
song_all_sheet_id = 742986052
new_song_sheet_id = 1439287617
group_sheet_id = 1706140349
vtuber_record_sheet_id = 918121082

def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scopes)
    return gspread.authorize(credentials)

def get_sheet(id):
    gss_client = auth_gss_client(auth_json_path, gss_scopes) #呼叫我們的函式

    #我們透過open_by_key這個method來開啟sheet
    workbook = gss_client.open_by_key(spreadsheet_key_path)
    sheet = workbook.get_worksheet_by_id(id)
    df = pd.DataFrame(sheet.get_all_records())

    return df, sheet

def clear_worksheet(worksheet):
  worksheet.clear()

def update_worksheet(df, worksheet):
  worksheet.update([df.columns.values.tolist()] + df.values.tolist())


def test():
    a = 1
    new_songs_df, new_songs_worksheet = get_sheet(1439287617) 

    print(new_songs_df)
    