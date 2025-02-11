#モジュールのインポート
import requests
from bs4 import BeautifulSoup
import tweepy
from PIL import Image
from io import BytesIO
import os
import datetime

#パスの取得
dir = os.path.dirname(__file__)
print(dir + "\BlackList.txt")

#ブラックリスト読み込み
with open(dir + "/BlackList.txt", encoding='UTF-8') as r:
    BlackList = r.readlines()

#改行コードを削除
BlackList = [i.replace("\n", "") for i in BlackList]

#人物が出るまでおまかせを取得する
while True:
    #淫夢wikiおまかせからURL取得
    load_url = "https://wiki.yjsnpi.nu/wiki/特別:おまかせ表示"
    html = requests.get(load_url)
    
    #HTML取得
    soup = BeautifulSoup(html.content, "html.parser")
    
    #出演作・画像の項目があるかどうか確認
    about = soup.find_all(id=".E5.87.BA.E6.BC.94.E4.BD.9C")
    img_address = soup.find('img', class_="mw-file-element").get('src')
    if not about == []:
        #人物名を取得
        name = soup.find("h1").text
        if not name in BlackList:
            if name == "KBTIT":
                name = "タクヤさん"
            print(name)
            break

#画像URL生成
img_url = "https://wiki.yjsnpi.nu" + img_address
print(img_url)
pic = requests.get(img_url)

#投稿時間まで待つ
while True:
    if datetime.datetime.now().minute == 0:
        break

#各種APIの読み込み
API_KEY = os.getenv("Inm_API_KEY")
API_KEY_SECRET = os.getenv("Inm_API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("Inm_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("Inm_ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("Inm_BEARER_TOKEN")

#クライアントオブジェクトの作成
client = tweepy.Client(
    bearer_token = BEARER_TOKEN,
    consumer_key = API_KEY,
    consumer_secret = API_KEY_SECRET,
    access_token = ACCESS_TOKEN,
    access_token_secret = ACCESS_TOKEN_SECRET
)

# APIの認証
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#認証オブジェクト生成
api = tweepy.API(auth)

#画像オブジェクト生成
img = BytesIO(pic.content)
result_img = api.media_upload(filename='sample2.png', file=img)

#投稿
client.create_tweet(text=name + "　#真夏の夜の淫夢", media_ids=[result_img.media_id])
