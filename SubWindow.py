#sub window
import sys
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from Sub import sub_class
import csv
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


class Parents(object):
    text = ''
    venture = ''
    year3 = []
    total_income = ''
    summary_info_list  = ''
class main(Parents):
    venture = Parents.text

    # 크롬 드라이버 이용해서 가상환경 창으로 url보내서 띄워줌
    ## **개인파일저장소로 바꿔주세요 !!! **

    # 검색창 가져오고 입력된 기업이름 검색

    url_data = pd.read_csv("kor_to_eng.csv")
    current_url = ""
    for i in range(url_data.shape[0]):
        if venture == url_data.iloc[i, 1]:
            current_url = "https://www.venturein.or.kr/venturein/infor/C21210.do?venid=" + url_data.iloc[i, 0] + "&menu=1"

    req = requests.get(current_url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    # 업종명 가져오기
    summary_info = soup.find('div', {"class": "width_table pb80"})
    summary_info_list = summary_info.findAll('td')
    sil = str(summary_info_list[3])
    result = sil.split("\"3\">")[1]
    result = result.split("<")[0]
    print("업종명:", result)

    income_csv = pd.read_csv("output.csv")

    for i in range(0, income_csv.shape[0]):
        temp_save = income_csv.iloc[i][0]
        temp_save = temp_save.split(", '")[1]
        temp_save = temp_save.split("'")[0]
        if temp_save == venture:
            year3 = income_csv.iloc[i][1]
            year3 = year3.split(',')
            total_income = (income_csv.iloc[i])[2]
            break

    print("3년도 매출액 증가율", year3)

    print("3개년 증가율의 평균", total_income)
    # 예상수익 가져오기 끝

    # 업종코드 가져오기 시작

    upjong_code = sub_class()
    summary_info = upjong_code.eng_to_upjong(result)

    print("업종코드:", summary_info)

    # 업종코드 가져오기 끝

    # 업종코드로 PER가져오기

    df = pd.read_csv("업종코드.csv", encoding='utf-8')

    for i in range(0, df.shape[0]):
        if i == summary_info:
            naver_name = df["name"][i - 1]

    req = requests.get("https://finance.naver.com/sise/sise_group.nhn?type=upjong")

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    summary_info = soup.find('table', {"class": "type_1"})
    summary_info_list = summary_info.findAll('a')

    star1 = str(summary_info_list)

    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    result = hangul.sub('', star1)
    data = result.split()

    for i in range(0, len(data)):
        if data[i] == "서비스":
            data[i] = "IT서비스"
        if data[i] == naver_name:
            save = summary_info_list[i]

    save2 = str(save).split("\"")

    save3 = "https://finance.naver.com" + save2[1]

    save3 = save3.replace("amp;", "")

    req = requests.get(save3)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    # 업종명 가져오기
    summary_info = soup.find('div', {"class": "name_area"})
    summary_info_list = summary_info.find('a')
    summary_info_list = str(summary_info_list).split("href=\"")[1]
    summary_info_list = summary_info_list.split("\">")[0]
    summary_info_list = "https://finance.naver.com" + summary_info_list

    req = requests.get(summary_info_list)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    summary_info = soup.find('table', {"summary": "동일업종 PER 정보"})
    summary_info_list = summary_info.find('em')

    print("per : ", summary_info_list.text)

    if total_income != 'x':
        print("엑싯 벨류 : ", float(total_income) * float(summary_info_list.text))
    else:
        print("데이터 부족으로 인한, 엑싯 벨류 계산 불가.")

    header = ['venture_name', 'three-year sales growth rate', 'average three-year growth rate', 'per']
    with open('filename.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        writer.writerow(header)
        writer.writerow([venture, year3, total_income, summary_info_list.text])
        save_all_data = [venture, year3, total_income, summary_info_list.text]
    Parents.venture = venture
    Parents.year3 = year3
    Parents.total_income = total_income
    Parents.summary_info_list = summary_info_list.text
class Window(Parents, QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sub Window')
        self.setGeometry(100, 100, 200, 100)
        layout = QVBoxLayout()
        layout.addStretch(1)
        edit = QLineEdit()
        font = edit.font()
        font.setPointSize(20)
        edit.setFont(font)
        self.edit = edit
        subLayout = QHBoxLayout()

        btnOK = QPushButton("확인")
        btnOK.clicked.connect(self.onOKButtonClicked)
        btnCancel = QPushButton("취소")
        btnCancel.clicked.connect(self.onCancelButtonClicked)
        layout.addWidget(edit)

        subLayout.addWidget(btnOK)
        subLayout.addWidget(btnCancel)
        layout.addLayout(subLayout)
        layout.addStretch(1)
        self.setLayout(layout)


    def return_edit_text(self):
        return Parents.text

    def onOKButtonClicked(self):
        Parents.text=self.edit.text()
        main()
        self.accept()
        self.ex=MyTab()



    def onCancelButtonClicked(self):
        self.reject()

    def showModal(self):
        return super().exec_()



class MyTab(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        tabs = QTabWidget()
        tabs.addTab(ventureTab(), 'VentureTab')
        tabs.addTab(graphTab(), 'GraphTab')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)
        self.setLayout(vbox)

        self.setWindowTitle('QTabWidget')
        self.setGeometry(300, 300, 1000, 1000)
        self.show()

class ventureTab(Parents, QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        name = QLabel('*업종명*')
        Venturename = QLabel(Parents.text)
        per = QLabel('per')
        ventureper = QLabel(Parents.summary_info_list)
        exitButton = QPushButton('exit', self)

        vbox = QVBoxLayout()
        vbox.addWidget(name)
        vbox.addWidget(Venturename)
        vbox.addWidget(per)
        vbox.addWidget(ventureper)
        vbox.addWidget(exitButton)
        vbox.addStretch()
        self.setLayout((vbox))

class graphTab(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        cb = QComboBox()
        cb.addItem('Graph1')
        cb.addItem('Graph2')
        cb.addItem('Graph3')
        cb.activated[str].connect(self.onComboBoxChanged)
        layout.addWidget(cb)
        vbox = QVBoxLayout()
        vbox.addWidget(cb)
        vbox.addWidget(self.canvas)
        self.setLayout((vbox))
        self.onComboBoxChanged(cb.currentText())


    def onComboBoxChanged(self, text):
        if text == 'Graph1':
            self.doGraph1()
        elif text == 'Graph2':
            self.doGraph2()
        elif text == 'Graph3':
            self.doGraph3()

    def doGraph1(self):
            x = np.arange(0, 10, 0.5)
            y1 = np.sin(x)
            y2 = np.cos(x)

            self.fig.clear()
            ax = self.fig.add_subplot(111)
            ax.plot(x, y1, label="sin(x)")
            ax.plot(x, y2, label="cos(x)", linestyle="--")

            ax.set_xlabel("x")
            ax.set_xlabel("y")

            ax.set_title("sin & cos")
            ax.legend()

            self.canvas.draw()

    def doGraph2(self):
            X = np.arange(-5, 5, 0.25)
            Y = np.arange(-5, 5, 0.25)
            X, Y = np.meshgrid(X, Y)
            Z = X ** 2 + Y ** 2

            self.fig.clear()

            ax = self.fig.gca(projection='3d')
            ax.plot_wireframe(X, Y, Z, color='black')
            self.canvas.draw()

    def doGraph3(self):
            years = ['2018', '2019', '2020']
            values = [100, 400, 900]

            self.fig.clear()
            ax = self.fig.add_subplot(111)
            ax.plot(years, values, label="3 years data")

            ax.set_xlabel("year")
            ax.set_ylabel("sales growth rate")

            ax.set_title("the growth rate of sales over the last three years")
            ax.legend()

            self.canvas.draw()