import pandas as pd

def create_txt(filestream, excel_file):
    excel = pd.read_excel(excel_file)
    
    for kor_sent, eng_sent in zip(excel['원문'], excel['번역문']):
        line = kor_sent + "\t" + eng_sent + "\n"
        filestream.write(line)

#once
f = open("kor_eng.txt", 'w')
create_txt(f, "/home/ubuntu/intaek/공모전/한영_말뭉치/3_문어체_뉴스(1)_200226.xlsx")
create_txt(f, "/home/ubuntu/intaek/공모전/한영_말뭉치/3_문어체_뉴스(2)_200226.xlsx")
create_txt(f, "/home/ubuntu/intaek/공모전/한영_말뭉치/3_문어체_뉴스(3)_200226.xlsx")
create_txt(f, "/home/ubuntu/intaek/공모전/한영_말뭉치/3_문어체_뉴스(4)_200226.xlsx")
create_txt(f, "/home/ubuntu/intaek/공모전/한영_말뭉치/4_문어체_한국문화_200226.xlsx")
create_txt(f, "/home/ubuntu/intaek/공모전/한영_말뭉치/6_문어체_지자체웹사이트_200226.xlsx")
f.close()

#문장 살펴보기
f = open("kor_eng.txt", 'r', encoding='utf-8')
lines = f.readlines()
print(len(lines))
print(lines[:10])

#문장 개수
f = open("kor_eng.txt", 'r')
print(len(f.readlines()))

#가장 긴 문장의 길이
max_line = ""
for line in f.readlines():
    if len(line) > len(max_line):
        max_line = line

print(len(max_line))

    
