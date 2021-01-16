from keras.preprocessing import image
import numpy as np
from keras import models
import json
from PIL import Image

def find_pos_from_json(json_path):
    """
    json_path: box_size를 추출할 파일

    description: 각 사진에 대한 json 파일에서 커팅할 box_size를 검색하여 반환 
    """
    
    try:
        with open(json_path, "r") as j:
            info = json.load(j)
            box_size = info['regions'][0]['boxcorners'] #box size 추출

    except:
        print("No such json file: " + json_path)
        return

    return box_size

def cutting_img_train(img_path, box_size):

    #이미지를 열어 자르고 저장
    img = Image.open(img_path)
    try:
        img_c = img.crop(box_size) 

    except:
        print("crop() error")
        pass
    
    return img_c

def image_predictor(img_path, box_size, saved_model, target_size=(150, 150)):
    #box size는 box를 그려주는 두 점에 대한 x축, y축 좌표를 가지고 있어야 함 
    assert len(box_size) == 4

    classes = ['43기념관', '518민주묘지상징탑', '63빌딩', '83타워', '경주타워', 
               '공산정', '광개토대왕동상', '광안대교', '국립과천과학관', '국립산악박물관', 
               '국립세종도서관', '근대역사박물관', '김대중노벨평화상기념관', '남산타워', '롯데월드타워', 
               '백남준아트센터', '부산타워', '송도G타워', '송도포스코타워', '여수세계박람회스카이타워', 
               '영도대교', '율곡이이동상', '이순신장군동상', '인천대교', '첨성대', 
               '풍남문', '하멜등대', '한빛탑', '해운대아이파크', '호미곶등대']

    img_c = cutting_img_train(img_path, box_size)
    # img = image.load_img(img_path, target_size=target_size)
    img_c = img_c.resize(target_size)
    img_tensor = image.img_to_array(img_c)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    model = models.load_model(saved_model)
    result = model.predict(img_tensor)

    return classes[np.argmax(result)]
    

# predict

# img_path = "/home/ubuntu/intaek/랜드마크/롯데월드타워/HF030004_0000_0328.jpg"
# json_path = "/home/ubuntu/intaek/랜드마크/롯데월드타워/HF030004_0000_0328.json"
# saved_model = "/home/ubuntu/intaek/Training_image.h5"
# classes_json_path = "/home/ubuntu/intaek/landmarks_info.json"

# box_size = find_pos_from_json(json_path)
# answer_class = image_predictor(img_path, box_size, saved_model)

# with open(classes_json_path, 'r', encoding='utf-8') as j:
#     info = json.load(j)
# print("이름: ", info[answer_class]['name'])
# print("설명: ", info[answer_class]['description'])
# print("주소: ", info[answer_class]['address'])
# print("관련어: ", info[answer_class]['related_term'])
    



