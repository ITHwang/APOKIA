import os, shutil
import sys
sys.path.append("../image") #해당 경로에 있는 .py 코드 불러오기
from image_cut_split import image_cut_split
import image_trainer
import warnings
warnings.filterwarnings(action='ignore')
import matplotlib.pyplot as plt


#경로 설정
load_dir = "../랜드마크"
cut_dir = "../cut_picture"
split_dir = "../split_picture"
train_split_path = os.path.join(split_dir, "train")
validation_split_path = os.path.join(split_dir, "validation")
test_split_path = os.path.join(split_dir, "test")

#클래스 구하기
classes = os.listdir(load_dir)
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

# Preprocessing -> at first trial
for i, _class in enumerate(classes):
    tmp = image_cut_split(_class, load_dir, cut_dir, split_dir)
    tmp.cutting_imgs()
    tmp.split_data(0.5)
    print("%d번째 랜드마크 [%s] 완료" %(i+1, _class))

#=========읽을 수 있는 사진인지 확인하기===========
def check_pics(split, split_path):
    classes = os.listdir(split_path)
    for _class in classes:
        class_path = os.path.join(split_path, _class)
        pics = os.listdir(class_path)
        
        for pic in pics:
            pic_path = os.path.join(class_path, pic)
            try:
                res = plt.imread(pic_path)
            except:
                print("Cannot open jpg: ", pic)
                os.remove(pic_path)

        print(split + " 내 " + _class + " 완료")
                
# check_pics("train", train_split_path)
# check_pics("validation", validation_split_path)
# check_pics("test", test_split_path)
#==================================================

train_gen, val_gen = image_trainer.generator(train_split_path = train_split_path, 
                               validation_split_path = validation_split_path, 
                               classes = classes)
image_trainer.trainer(second_dense_unit = len(classes), 
        train_gen = train_gen, val_gen = val_gen, 
        save_name = "Training_image.h5")