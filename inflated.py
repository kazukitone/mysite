import os
import glob
import numpy as np
from keras.preprocessing.image import ImageDataGenerator,load_img, img_to_array, array_to_img

# 画像を拡張する関数
def draw_images(generator, x, dir_name, index):
    save_name = 'extened-' + str(index)
    g = generator.flow(x, batch_size=1, save_to_dir=output_dir,
                       save_prefix=save_name, save_format='jpeg')

    # 1つの入力画像から何枚拡張するかを指定（今回は3枚）
    for i in range(3):
        bach = g.next()

# 出力先フォルダの設定
output_dir = "./image/somen2"

if not(os.path.exists(output_dir)):
    os.mkdir(output_dir)

# 拡張する画像の読み込み
images = glob.glob(os.path.join("./image/somen", "*.jpg"))

# ImageDataGeneratorを定義
datagen = ImageDataGenerator(rotation_range=20,
                            width_shift_range=0,
                            shear_range=0,
                            height_shift_range=0,
                            zoom_range=0,
                            horizontal_flip=True,
                            fill_mode="nearest",
                            channel_shift_range=40)　

# 読み込んだ画像を順に拡張
for i in range(len(images)):
    img = load_img(images[i])
    img = img.resize((250,250))
    x = img_to_array(img)
    x = (x, axis=0)
    draw_images(datagen, x, output_dir, i)