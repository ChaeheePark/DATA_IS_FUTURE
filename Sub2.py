import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd

def popup():
    address = "https://www.venturein.or.kr/popup/BusinessCode.do?targetFormName=listForm&targetForm1=upjcod&targetForm2=upjnam"
    req = requests.get(address)
    html = req.text
    html = str(html).replace("type=\"text\" value=\"\"","type=\"text\" value=\"그 외 기타 정보 서비스업\"")
    html.replace("Keycode(event);","true")

    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select("#listForm > div > div > fieldset > ul.form_pop.mb15 > li:nth-child(2) > input[type=image]")

    print(elements)


popup()