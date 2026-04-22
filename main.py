#モジュールのインポート
import requests
from bs4 import BeautifulSoup
import tweepy
from PIL import Image
from io import BytesIO
import os
import csv
import datetime
import random

#パスの取得
dir = os.path.dirname(__file__)

#ブラックリスト読み込み
with open(dir + "/BlackList.txt", encoding="UTF-8") as r:
    BlackList = r.readlines()

#人気者リスト読み込み
with open(dir + "/Popular.txt", encoding="UTF-8") as r:
    Popular = r.readlines()

#改行コードを削除
BlackList = [i.replace("\n", "") for i in BlackList]
Popular = [i.replace("\n", "") for i in Popular]

#人物が出るまでおまかせを取得する
while True:
    if random.randint(1,100) <= 3:
        name = Popular[random.randint(0, len(Popular))-1]
        load_url = "https://wiki.yjsnpi.nu/wiki/" + name
    else:
        #淫夢wikiおまかせからURL取得
        load_url = "https://wiki.yjsnpi.nu/wiki/特別:おまかせ表示"

    #HTML取得
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")

    #人物かどうかの判定
    target_href = "https://wiki.yjsnpi.nu/wiki/登場人物"
    found = False
    for a in soup.find_all("a", href=True):
        if "登場人物一覧" in a.get_text():
            found = True
            break

    if found:
    #要素を検索
        img_element = soup.find("img", class_="mw-file-element").get('src')
        #人物名を取得
        name = soup.find("h1").text

        #名前がブラックリストに入っていればループの最初へ
        if name in BlackList:
            continue
            
        #リネーム
        with open(dir + "/Rename.csv", encoding="UTF-8") as r:
            Rename = csv.reader(r)
            for n in Rename:
                if name == n[0]:
                    name = n[1]

        print(name)
        break

#画像URL生成
img_url = "https://wiki.yjsnpi.nu" + img_element
print(img_url)
pic = requests.get(img_url)

#投稿時間まで待つ
while True:
    if datetime.datetime.now().minute == 0:
        break
        
#日本時間の日付を取得
day = str(datetime.datetime.now().month) + "." + str(datetime.datetime.now().day + int((datetime.datetime.now().hour + 9) / 24))
print(day)

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
result_img = api.media_upload(filename="homo.png", file=img)

#投稿
client.create_tweet(text=name + "　#真夏の夜の淫夢", media_ids=[result_img.media_id])
