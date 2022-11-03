import config

# スプシ設定----------------------------------------------------------------------------------------------------------
import gspread
# ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials
# 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# 認証情報設定
# ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('mk8developers.json', scope)
# OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)
# 共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
# https://docs.google.com/spreadsheets/d/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/edit#gid=0
SPREADSHEET_KEY = config.SPREADSHEET_KEY
# 共有設定したスプレッドシートを開く
workbook = gc.open_by_key(SPREADSHEET_KEY)
# --------------------------------------------------------------------------------------------------------------------