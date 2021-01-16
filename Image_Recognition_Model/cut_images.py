# 클래스마다 jpg, json 포함 7,000개라서 2,000개로 줄임

import os, shutil

base_path = "..\랜드마크"
dirs = os.listdir(base_path)

#각 클래스마다 1000개만 남기고 삭제
n_files = 2000 #사진마다 json 파일 있음(1000 + 1000)
for dir in dirs:
    dir_path = os.path.join(base_path, dir)
    files = os.listdir(dir_path) 
    files = files[n_files:]

    for _file in files:
        file_path = os.path.join(dir_path, _file)
        os.remove(file_path)
    
    print("%s 제거 완료" %dir)

# 각 클래스 파일 내 사진 및 json 개수 세기
sum = 0
for dir in dirs:
    dir_path = os.path.join(base_path, dir)
    files = os.listdir(dir_path) 
    n_files = 0
    for _file in files:
        n_files += 1
    sum += n_files
    print("%s의 개수: %d" %(dir, n_files))

print("총 개수: ", sum)
    