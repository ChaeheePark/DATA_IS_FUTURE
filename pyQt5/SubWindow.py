#sub window
import sys
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class Parents(object):
    text = ''

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
        return self.edit.text(self)

    def onOKButtonClicked(self):
        Parents.text=self.edit.text()
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
        ventureper = QLabel('10.65')
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