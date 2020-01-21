import os
import cv2
from flask import Flask,  request, redirect, url_for, render_template,  flash
from werkzeug.utils  import secure_filename
from keras.models import Sequential, load_model
from keras.preprocessing import image
import tensorflow as tf
import numpy as np

classes = ["らーめん", "そば", "うどん", "パスタ"]
num_classes = len(classes)
image_size1 = 128
image_size2 = 150

UPLOAD_FOLDER = "static"
ALLOWED_EXTENSION = set(["png", "jpg", "jepg", "gif"])

app = Flask(__name__)

def allowed_file(filename):
    #filenameの.より後ろの文字列がALLOWED_EXTENSIONのどれかに該当するかどうか確認
    return "." in  filename and filename.resplit(".", 1)[1].lower() in ALLOWED_EXTENSION


model = load_model("model.h5")#学習済モデルのロード

graph = tf.get_default_graph()#kerasのバグのために必要なコード

@app.route("/", methods = ["GET", "POST"])#ページにアクセスした時にhtmlファイルを読み込む、データをサーバーへ送信する
def upload_file():
    global graph#kerasのバグのため必要
    with graph.as_default():#kerasのバグのために必要
        if request.method == "POST":#web上のフォームから送信したデータを扱うための関数,POSTの時以下のコードが実行される
            if  "file" not in request.files:#ファイルがない場合、flashが実行される
                flash("ファイルがありません")
                return redirect(request.url)
            file = request.files["file"]
            if  file and allowed_file(file.filename):
                filename = secure_filename(file.filename)#ファイルに危険な文字列（<など、HTMLタグに影響がでる)がある場合に無効化
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                filepath = os.path.join(UPLOAD_FOLDER, filename)
            #うけとった画像を読み込み
                img = image.load_img(filepath, grayscale=True, target_size=(image_size1,image_size2))
                img = image.img_to_array(img)
                data = np.array([img])
                #変換したデータをモデルに渡して予測する
                result = model.predict(data)[0]
                predicted = result.argmax()
                pred_answer = "これは " + classes[predicted] + " です"

                return render_template("index.html",answer=pred_answer)

        return render_template("index.html",answer="")


if __name__ == "__main__":
    app.run()