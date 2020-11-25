import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

address = "https://www.venturein.or.kr/venturein/infor/C21210.do?venid=%20core0510&menu=1"
req = requests.get(address)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

summary_info = soup.find('div', {"class":"width_table pb80"})
summary_info = summary_info.findAll("tr")[2]
summary_info = summary_info.find("td")
summary_info = str(summary_info).split("\"3\">")[1]
summary_info = str(summary_info).split("</td>")[0]
print(summary_info)

csv_Data = pd.read_csv("d.csv")
Data_name_col = csv_Data.iloc[:,9:11]
print(Data_name_col)

for i in range(Data_name_col.shape[0]):
    if Data_name_col.iloc[i,1] == summary_info:
        find_index = Data_name_col.iloc[i,0]


while find_index>100:
    find_index = find_index / 10

find_index = int(find_index)