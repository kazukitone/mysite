
from flickrapi import FlickrAPI
#ネット上からファイルをダウンロードし保存
from urllib.request import urlretrieve
#データ出力を見やすくすることが可能
from pprint import  pprint
#sys→システムに関する処理をまとめたライブラリ
import os,time,sys

#APIキーとシークレットを指定する
key= "52b0ae26d59c9873387cfe7a2a809ac6"
secret= "5d5b795c115c68f0"
wait_time=2#リクエストを発行するインターバル

def main():
    go_download("パスタ","pasta") #現在のpath（ディレクトリの場所を示す文字列）を表示
    
def go_download(keyword,dir):
    #画像の保存パス
    savedir="./image/"+dir#画像の保存ディレクトリを作成
    if not os._exists(savedir):#pathが存在しているか確認
        os.mkdir(savedir)#新しいディレクトリを作成
    #APIでダウンロード
    flickr=FlickrAPI(key,secret,format="parsed-json")#key, secret, formatの設定
    res=flickr.photos.search(#検索条件の設定
        text="pasta",
        per_page=300,
        media="photos",
        sort="relevance",#関連順に調べる
        safe_search=1,#1は安全
        extras="url_q,license")#余分に取得する情報(ダウンロード用のURL、ライセンス)
    
    #検索結果を確認
    photos=res["photos"]
    pprint(photos)
    try:
        #一枚ずつ画像をダウンロード
        for i ,photo in enumerate(photos["photo"]):#enumerate→１枚ずつ画像を取得
            url_q=photo["url_q"]
            filepath=savedir+"/"+photo["id"]+".jpg"#pathの設定
            if os.path.exists(filepath):continue
            print(str(i+1)+":download=",url_q)
            urlretrieve(url_q,filepath)
            time.sleep(wait_time)
           
    except:
        import traceback#スタックトレース（エラーの過程）の表示
        traceback.print_exc()
            
if __name__=="__main__":
    main()