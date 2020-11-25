import time
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from Sub import sub_class
import csv

venture=input("찾고 싶은 벤처 기업명을 입력해 주세요: ")

#크롬 드라이버 이용해서 가상환경 창으로 url보내서 띄워줌
## **개인파일저장소로 바꿔주세요 !!! **

#검색창 가져오고 입력된 기업이름 검색

url_data = pd.read_csv("kor_to_eng.csv")


for i in range(url_data.shape[0]):
    if venture == url_data.iloc[i,1]:
        current_url = "https://www.venturein.or.kr/venturein/infor/C21210.do?venid="+url_data.iloc[i,0]+"&menu=1"

print(current_url)
req = requests.get(current_url)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

#업종명 가져오기
summary_info = soup.find('div', {"class":"width_table pb80"})
summary_info_list = summary_info.findAll('td')
sil = str(summary_info_list[3])
result = sil.split("\"3\">")[1]
result = result.split("<")[0]
print("업종명:",result)

income_csv = pd.read_csv("output.csv")

for i in range(0,income_csv.shape[0]):
    temp_save = income_csv.iloc[i][0]
    temp_save = temp_save.split(", '")[1]
    temp_save = temp_save.split("'")[0]
    if temp_save == venture:
        year3 = income_csv.iloc[i][1]
        year3 = year3.split(',')
        total_income = (income_csv.iloc[i])[2]
        break

print("3년도 매출액 증가율",year3)

print("3개년 증가율의 평균",total_income)
#예상수익 가져오기 끝

#업종코드 가져오기 시작


upjong_code = sub_class()
summary_info = upjong_code.eng_to_upjong(result)

print("업종코드:",summary_info)

#업종코드 가져오기 끝

#업종코드로 PER가져오기


df = pd.read_csv("업종코드.csv", encoding='utf-8')

for i in range(0,df.shape[0]):
    if i == summary_info:
        naver_name = df["name"][i-1]



req = requests.get("https://finance.naver.com/sise/sise_group.nhn?type=upjong")

html = req.text
soup = BeautifulSoup(html, 'html.parser')


summary_info = soup.find('table', {"class":"type_1"})
summary_info_list = summary_info.findAll('a')


star1 = str(summary_info_list)

hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
result = hangul.sub('',star1)
data = result.split()

for i in range(0,len(data)):
    if data[i] == "서비스":
        data[i] = "IT서비스"
    if data[i] == naver_name:

        save = summary_info_list[i]

save2 = str(save).split("\"")


save3 = "https://finance.naver.com" + save2[1]

save3 = save3.replace("amp;","")

req = requests.get(save3)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

#업종명 가져오기
summary_info = soup.find('div', {"class":"name_area"})
summary_info_list = summary_info.find('a')
summary_info_list = str(summary_info_list).split("href=\"")[1]
summary_info_list = summary_info_list.split("\">")[0]
summary_info_list = "https://finance.naver.com"+summary_info_list

req = requests.get(summary_info_list)
html = req.text
soup = BeautifulSoup(html, 'html.parser')
summary_info = soup.find('table', {"summary":"동일업종 PER 정보"})
summary_info_list = summary_info.find('em')

print("per : ",summary_info_list.text)

if total_income != 'x':
    print("엑싯 벨류 : ",float(total_income) * float(summary_info_list.text))
else:
    print("데이터 부족으로 인한, 엑싯 벨류 계산 불가.")

header = ['venture_name','three-year sales growth rate', 'average three-year growth rate', 'per']
with open('filename.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"')
    writer.writerow(header)
    writer.writerow([venture, year3, total_income, summary_info_list.text])