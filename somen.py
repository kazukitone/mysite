from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import  pprint
import os,time,sys

#APIキーとシークレットを指定する
key= "52b0ae26d59c9873387cfe7a2a809ac6"
secret= "5d5b795c115c68f0"
wait_time=2

def main():
    go_download("そうめん","somen") 
    
def go_download(keyword,dir):
    #画像の保存パス
    savedir="./image/"+dir
    if not os._exists(savedir):
        os.mkdir(savedir)
    #APIでダウンロード
    flickr=FlickrAPI(key,secret,format="parsed-json")
    res=flickr.photos.search(
        text="somen",
        per_page=300,
        media="photos",
        sort="relevance",
        safe_search=1,
        extras="url_q,license")
    
    #検索結果を確認
    photos=res["photos"]
    pprint(photos)
    try:
        #一枚ずつ画像をダウンロード
        for i ,photo in enumerate(photos["photo"]):
            url_q=photo["url_q"]
            filepath=savedir+"/"+photo["id"]+".jpg"
            if os.path.exists(filepath):continue
            print(str(i+1)+":download=",url_q)
            urlretrieve(url_q,filepath)
            time.sleep(wait_time)
           
    except:
        import traceback
        traceback.print_exc()
            
if __name__=="__main__":
    main()