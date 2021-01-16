import os
from keras.preprocessing.image import ImageDataGenerator
from keras import models
import tensorflow as tf

split_dir = "../split_picture" #image_cut_split에 의해 생성된 directory
test_split_path = os.path.join(split_dir, "test")

classes = os.listdir(test_split_path)
if '.ipynb_checkpoints' in classes:
    classes.remove('.ipynb_checkpoints')

#================
# 클래스 50개는 정확도가 낮음... 30개로 도전
remove_class = ['아르피아타워', '코오롱스카이타워', '메타폴리스', '천안펜타포트', '구봉산전망대', 
                '롯데시티호텔제주', '공지천구름다리', 'KDB생명빌딩', '수성SK리더스뷰', '한국전력공사본사', 
                '구리타워', '울산대교전망대', '엑스포타워', '스카이베이호텔', '독립기념관겨레의탑',
                '프라이부르크전망대', '월영교', '웅비탑', '영남루', '촉석루']

for item in remove_class:
    classes.remove(item)
#================

print("클래스: ", classes)
print("클래스 개수: ", len(classes))

test_datagen = ImageDataGenerator(rescale = 1./255)

test_gen = test_datagen.flow_from_directory(
    test_split_path,
    target_size=(150, 150),
    batch_size=20,
    classes = classes
)

with tf.device('/gpu:0'):
    model = models.load_model("Training_image.h5")
    test_loss, test_acc = model.evaluate_generator(test_gen, steps=50)
print("test acc: ", test_acc)
