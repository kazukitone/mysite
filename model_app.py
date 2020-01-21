import os
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.utils.np_utils import to_categorical
from keras.layers import Dense, Dropout, Flatten, Input
from keras.applications.vgg16 import VGG16
from keras.models import Model, Sequential
from keras import optimizers
from keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint
keras.backend.clear_session()
 
 
# 各麺類配列格納
noodle_list = ["ramen3", "udon3", "soba3", "pasta3"]
print(noodle_list)
print(len(noodle_list))
 
 
# 各麺類の画像ファイルパスを配列で取得する関数
def get_path_noodle(noodle):
  path_noodle = glob.glob('./image/'+noodle+'/*')
  return path_noodle
 
 
# 各麺類の画像データndarray配列を取得する関数
def get_img_noodle(noodle):
  path_noodle = get_path_noodle(noodle)
  
  img_noodle = []
  for i in range(len(path_noodle)):
    # 画像の読み取り
    img = cv2.imread(path_noodle[i])
    # img_sakuraiに画像データのndarray配列を追加していく
    img_noodle.append(img)
  return img_noodle 
 
 
# 各麺類の画像データを合わせる
X = []
y = []
for i in range(len(noodle_list)):
    print(noodle_list[i] + ":" + str(len(get_img_noodle(noodle_list[i]))))
    X += get_img_noodle(noodle_list[i])
    y += [i]*len(get_img_noodle(noodle_list[i]))
X = np.array(X)
y = np.array(y)
 
print(X.shape)
 
# ランダムに並び替え
rand_index = np.random.permutation(np.arange(len(X)))
 
# 上記のランダムな順番に並び替え
X = X[rand_index]
y = y[rand_index]
 
# データの分割（トレインデータが8割）
X_train = X[:int(len(X)*0.8)]
y_train = y[:int(len(y)*0.8)]
X_test = X[int(len(X)*0.8):]
y_test = y[int(len(y)*0.8):]
 
# one-hot表現に変換
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)
 
# モデル


input_tensor = Input(shape=(128, 150, 3))
vgg16 = VGG16(include_top=False, weights='imagenet', input_tensor=input_tensor)

top_model = Sequential()
top_model.add(Flatten(input_shape=vgg16.output_shape[1:]))
top_model.add(Dense(512, activation='relu'))
top_model.add(Dropout(0.5))
top_model.add(Dense(len(noodle_list), activation='softmax'))
 
model = Model(inputs=vgg16.input, outputs=top_model(vgg16.output))
 
# modelの16層目までがvggのモデル
for layer in model.layers[:15]:
    layer.trainable = False
 
# モデルの読み込み
# model.load_weights('model.h5')
 
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.SGD(lr=1e-4, momentum=0.9),
              metrics=['accuracy'])
 
model.summary()
es_cb = EarlyStopping(monitor='val_loss', patience=2, verbose=1, mode='auto')
tb_cb = TensorBoard(log_dir="./tensorlog", histogram_freq=1) 
history = model.fit(X_train, y_train, batch_size=150, epochs=20, verbose=1,validation_data=(X_test, y_test),  callbacks=[es_cb, tb_cb]) 

# モデルの保存
# model.save_weights('model.h5');
model.save('./model.h5')
 
 
# 精度の評価（適切なモデル名に変えて、コメントアウトを外してください）
scores = model.evaluate(X_test, y_test, verbose=1)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])
 
# acc, val_accのプロット
plt.plot(history.history['acc'], label='acc', ls='-')
plt.plot(history.history['val_acc'], label='val_acc', ls='-')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(loc='best')
plt.show()