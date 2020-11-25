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
        print(data)
        with open('kor_to_eng.csv','a',encoding="utf8") as file:
            writer = csv.writer(file)
            writer.writerow(data)

        #page_id = "https://www.venturein.or.kr/venturein/infor/C21210.do?venid="+data[0]+"&menu=1"
