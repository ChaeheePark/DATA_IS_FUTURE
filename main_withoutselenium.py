import requests
from bs4 import BeautifulSoup
import csv


for i in range(1,3909):
    address = "https://www.venturein.or.kr/venturein/infor/C22100.do?pageIndex=" + str(i)

    req = requests.get(address)

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    summary_info = soup.find('div', {"class":"board_table pb50"})
    summary_info_list = summary_info.findAll('td')

    for i in range(0,10):
        data = str(summary_info_list[1 + i * 5]).split("venid=")[1]
        data2 = data.split("menu=1\">")[1]
        data2 = data2.split("</a")[0]

        data = data.split("&amp")[0]
        data = data.replace(' ','')
        data = [data, data2]

        with open('output.csv','a',encoding="utf8") as file:
            writer = csv.writer(file)
            writer.writerow(data)

        page_id = "https://www.venturein.or.kr/venturein/infor/C21221.do?venid="+data[0]+"&menu=1"
        print(page_id)

        req = requests.get(page_id)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        summary_info = soup.find_all('td', {"class": "t_center"})
        summary=[]
        count = 3
        sum = 0
        for i in range(1,4):
            if summary_info[i].text=='':
                summary.append(0.0)
            else:
                summary.append(float(summary_info[i].text))
            if summary[i-1]==0.0:
                count = count - 1
            sum += summary[i-1]
        if count == 0:
            count = 1
        sum = sum / count
        print("3개년 증가율의 평균", sum)
        income = soup.find_all('td', {"class": "t_right"})
        try:
            if len(income[7].text) > 3:
                income = (income[7].text).replace(',', '')
            income=int(income[7].text)
            if income == 0:
                print('최근 수익이 없어 엑싯벨류를 예측하지 못합니다.')
                continue
            future_income = (float(sum / 100) * income) + income
            print("n년 후 예상 수익:", future_income)
        except IndexError:
            print('최근 수익이 없어 엑싯벨류를 예측하지 못합니다.')