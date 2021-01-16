#아래 클래스에 해당하는 정보들을 json 파일에서 추출하는 코드

import json
import os

classes = ['43기념관', '518민주묘지상징탑', '63빌딩', '83타워', '경주타워', 
            '공산정', '광개토대왕동상', '광안대교', '국립과천과학관', '국립산악박물관', 
            '국립세종도서관', '근대역사박물관', '김대중노벨평화상기념관', '남산타워', '롯데월드타워', 
            '백남준아트센터', '부산타워', '송도G타워', '송도포스코타워', '여수세계박람회스카이타워', 
            '영도대교', '율곡이이동상', '이순신장군동상', '인천대교', '첨성대', 
            '풍남문', '하멜등대', '한빛탑', '해운대아이파크', '호미곶등대']

Landmarks = dict()

base_path = "../랜드마크" #jpg, json이 저장되어있는 raw dataset directory
for _class in classes:
    #json 파일 찾아서 정보 가져오기
    class_path = os.path.join(base_path, _class)

    #json 파일 아무거나 가져오기
    json_path = ""
    for _file in os.listdir(class_path):
        if _file[-4:] == "json":
            json_path = os.path.join(class_path, _file)
            break
    
    #json 파일에서 가져온 정보로 각 class마다 dictionary 만들기 
    tmp = dict()
    with open(json_path, "r") as j:
        info = json.load(j)
        tmp["name"] = info['regions'][0]['tags'][5][9:]
        tmp["description"] = info['regions'][0]['sem_ext'][0]['value']
        tmp["address"] = info["regions"][0]['sem_ext'][1]['value']
        tmp["related_term"] = info["regions"][0]['sem_ext'][2]['value']

    Landmarks[_class] = tmp

with open('../landmarks_info.json', 'w',
          encoding='utf-8') as make_file:
    json.dump(Landmarks, make_file, indent="\t", ensure_ascii=False)
