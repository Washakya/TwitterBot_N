#モジュールのインポート
import requests
from bs4 import BeautifulSoup
import tweepy
from PIL import Image
import io
from io import BytesIO

#各種APIのセットアップ
API_KEY = "vn0sBOnejrJ4r72gFwVdMugdd"
API_SECRET = "LO98Pv5nZYGkJboBgA7OunIHPka1Ow20jTZ8EmCTerxmfxNEMA"
ACCESS_TOKEN = "1486869932268826625-tpkxWQre2DmjoiwguWctQtkFCfEuJS"
ACCESS_TOKEN_SECRET = "Unrorr8Xc2crr2w3qTb2yrPxmixOfxuviavroqvfQnKUw"

# APIの認証
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#認証オブジェクト生成
api = tweepy.API(auth)

#人物が出るまでおまかせを取得する
while True:
    #淫夢wikiおまかせからURL取得
    load_url = "https://wiki.yjsnpi.nu/wiki/特別:おまかせ表示"
    html = requests.get(load_url)
    
    #HTML取得
    soup = BeautifulSoup(html.content, "html.parser")
    
    #出演作・画像の項目があるかどうか確認
    about = soup.find_all(id=".E5.87.BA.E6.BC.94.E4.BD.9C")
    img_address = soup.find('img').get('src')
    if not about == []:
        #人物名を取得
        name = soup.find("h1").text
        print(name)
        break

#画像URL生成
img_url = "https://wiki.yjsnpi.nu" + img_address
print(img_url)
pic = requests.get(img_url)

#画像オブジェクト生成
img = BytesIO(pic.content)
result_img = api.media_upload(filename='sample2.png', file=img)

#投稿
api.update_status(status=name, media_ids=[result_img.media_id])
