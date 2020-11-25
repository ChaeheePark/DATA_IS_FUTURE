from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

venture=input("찾고 싶은 벤처 기업명을 입력해 주세요: ")

#크롬 드라이버 이용해서 가상환경 창으로 url보내서 띄워줌
## **개인파일저장소로 바꿔주세요 !!! **
chromedriver_dir = '../chromedriver'
driver = webdriver.Chrome(chromedriver_dir)
driver.get("https://www.venturein.or.kr/venturein/infor/C22100.do")

#검색창 가져오고 입력된 기업이름 검색
element = driver.find_element_by_name('purcmpnam')
element.send_keys(venture)
element.submit()
driver.find_element_by_xpath('//*[@id="listForm"]/fieldset/div[2]/table/tbody/tr/td[2]/a').click()


req = requests.get(driver.current_url)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

#업종명 가져오기
summary_info = soup.find('div', {"class":"width_table pb80"})
summary_info_list = summary_info.findAll('td')
sil = str(summary_info_list[3])
hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
result = hangul.sub('',sil)
print("업종명:", result)

#예상수익 가져오기
driver.find_element_by_xpath('//*[@id="contents"]/div[3]/ul/li[2]/a').click()
html = req.text
soup = BeautifulSoup(html, 'html.parser')
count=3
sum=0
percentages=[]
for i in range(3,6):
    pc = driver.find_element_by_xpath('//*[@id="contents"]/div[4]/div[2]/table/tbody/tr[1]/td[' + str(i) + ']').text
    if pc != '': #null값일때
        percentages.append(float(pc))
    else:
        percentages.append(0.0)
    if percentages[i-3]==0.0:
        count=count-1
    sum+=percentages[i-3]

if count==0:
    count=1
sum=sum/count
print("3개년 증가율의 평균",sum)

a=driver.find_element_by_xpath('//*[@id="contents"]/div[4]/div[3]/table/tbody/tr[1]/td[2]').text
income=int(a.replace(',',''))
#예외처리
if income==0:
    print("최근 수익이 없어 예측불가 하여 프로그램을 종료합니다.")
    exit()

future_income=(float(sum/100)*income)+income
print("n년 후 예상 수익:",future_income)

#예상수익 가져오기 끝

#업종코드 가져오기 시작

driver.get("https://www.venturein.or.kr/venturein/infor/C22100.do")
driver.find_element_by_xpath('//*[@id="listForm"]/fieldset/div[1]/ul/li[6]/span/a/img').click()

driver.switch_to.window(driver.window_handles[-1])

element = driver.find_element_by_name('upjcodnam')
element.send_keys(result)

driver.find_element_by_xpath('//*[@id="listForm"]/div/div/fieldset/ul[1]/li[2]/input').click()

req = requests.get(driver.current_url)

html = req.text
soup = BeautifulSoup(html, 'html.parser')

summary_info = driver.find_element_by_xpath('//*[@id="listForm"]/div/div/fieldset/div[2]/table/tbody/tr/td[1]/a').text


summary_info = int(int(summary_info) / 1000)
print("업종코드:",summary_info)

#업종코드 가져오기 끝

#업종코드로 PER가져오기

driver.close()
driver.switch_to.window(driver.window_handles[0])

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
        print(data[i])

        save = summary_info_list[i]

save2 = str(save).split("\"")


save3 = "https://finance.naver.com" + save2[1]

save3 = save3.replace("amp;","")

print(save3)

driver.get(save3)
driver.find_element_by_xpath('//*[@id="contentarea"]/div[4]/table/tbody/tr[1]/td[1]/div/a').click()

per_data = driver.find_element_by_xpath('//*[@id="tab_con1"]/div[5]/table/tbody/tr[1]/td/em').text

print("PER:",float(per_data))

print("예상 엑싯밸류 입니다:",float(per_data)*future_income)