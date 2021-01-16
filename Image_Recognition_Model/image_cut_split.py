import json
from PIL import Image
import matplotlib.pyplot as plt
import os, shutil

class image_cut_split:

    def __init__(self, class_name, load_path, cut_path, split_path):
        """
        load_path: 불러올 데이터 경로
        cut_path: 커팅 후 저장할 경로
        split_path: dataset split 후 저장할 경로
        description: raw image를 커팅 후 저장함. 
                    이후 train, validation, test dataset으로 분리함.
        """

        self.iter = 0 #가공된 사진들에 대한 구분 번호
        self.class_name = class_name

        self.load = load_path
        if not os.path.exists(self.load):
            print("No such file or directory: " + self.load)
            raise FileNotFoundError

        self.cut = cut_path
        if not os.path.exists(self.cut):
            os.makedirs(self.cut)

        #맨 처음 만들어진 클래스에서 split 폴더 생성
        self.split = split_path
        if not os.path.exists(self.split):
            os.makedirs(self.split)

        #load_path 내 해당 클래스 경로
        self.class_load_path = os.path.join(self.load, self.class_name)
        if not os.path.exists(self.class_load_path):
            print("No such file or directory: " + self.class_load_path)
            raise FileNotFoundError

        #cut_path 내 해당 클래스 경로
        self.class_cut_path = os.path.join(self.cut, self.class_name)
        if not os.path.exists(self.class_cut_path):
            os.makedirs(self.class_cut_path)    

        #split_path 내 경로
        self.train_split_path = os.path.join(self.split, "train")
        if not os.path.exists(self.train_split_path):
            os.makedirs(self.train_split_path)

        self.validation_split_path = os.path.join(self.split, "validation")
        if not os.path.exists(self.validation_split_path):
            os.makedirs(self.validation_split_path)

        self.test_split_path = os.path.join(self.split, "test")
        if not os.path.exists(self.test_split_path):
            os.makedirs(self.test_split_path)

    def find_pos_from_json(self, json_path):
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
  
    def cutting_img_train(self, img_path):
        """
        img_path: raw data 경로
    
        description: img_path와 이름이 같은 json 파일 내에서 추출한 box size대로 커팅 후 저장 
        """
    
        #가공하려는 이미지와 이름이 같은 json 파일에서 box size 추출
        json_path = img_path[:-3] + "json"
        box_size = self.find_pos_from_json(json_path)
    
        #이미지를 열어 자르고 저장
        img = Image.open(img_path)
        try:
            img_c = img.crop(box_size) 

        except:
            print("crop() error")
            pass
        try:
            img_c.save(self.class_cut_path + '/' + self.class_name + '.' + str(self.iter) + ".jpg")
        except:
            print("save() error")
            pass
    
    def cutting_imgs(self):
        """
        description: load_path 내 raw data들을 커팅한 후 저장
        """

        #load_path 내에 위치한 파일들 중 jpg만 골라내서 자르고 저장
        filenames = os.listdir(self.class_load_path)
        for filename in filenames:
            if filename[-3:] == "jpg" or filename[-3:] == "JPG":
                img_path = os.path.join(self.class_load_path, filename)
                self.cutting_img_train(img_path)
                self.iter += 1

            if self.iter % 200 == 0: 
                print("%d번째 완료" % self.iter)
        
    def split_data(self, train_rate):
        """
        train_rate: train에 할당할 비율. 나머지 비율에서 validation과 test가 반씩 나눠 갖는다.
        description: train, validation, test dataset 만들고 저장
        """

        #클래스마다 train, validation, test 폴더 생성
        train_dir =  os.path.join(self.train_split_path, self.class_name)
        if not os.path.exists(train_dir):
            os.makedirs(train_dir)

        validation_dir =  os.path.join(self.validation_split_path, self.class_name)
        if not os.path.exists(validation_dir):
            os.makedirs(validation_dir)

        test_dir =  os.path.join(self.test_split_path, self.class_name)
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
        
        #train_rate에 따라 dataset 사이즈 구하기
        n_files = len(os.listdir(self.class_cut_path))
        validation_rate = (1 - train_rate) / 2
        train_size = int(n_files * train_rate)
        validation_size = int(n_files * validation_rate)
        
        #train size만큼 복사
        fnames = [self.class_name + ".{}.jpg".format(i) for i in range(train_size)]
        for fname in fnames:
            src = os.path.join(self.class_cut_path, fname)
            dst = os.path.join(train_dir, fname)
            try:
                shutil.copyfile(src, dst)
            except:
                pass
        print("%s의 train 개수: %d" %(self.class_name, len(os.listdir(train_dir))))
        
        #validation size만큼 복사
        fnames = [self.class_name + ".{}.jpg".format(i) for i in range(train_size, train_size + validation_size)]
        for fname in fnames:
            src = os.path.join(self.class_cut_path, fname)
            dst = os.path.join(validation_dir, fname)
            try:
                shutil.copyfile(src, dst)
            except:
                pass
        print("%s의 validation 개수: %d" %(self.class_name, len(os.listdir(validation_dir))))

    
        #test size만큼 복사
        fnames = [self.class_name + ".{}.jpg".format(i) for i in range(train_size + validation_size, n_files)]
        for fname in fnames:
            src = os.path.join(self.class_cut_path, fname)
            dst = os.path.join(test_dir, fname)
            try:
                shutil.copyfile(src, dst)
            except:
                pass
        print("%s의 test 개수: %d" %(self.class_name, len(os.listdir(test_dir))))

        