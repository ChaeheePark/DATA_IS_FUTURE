#main window
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from SubWindow import Window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        layout.addStretch(1)
        label = QLabel("미지정")
        label.setAlignment(Qt.AlignCenter)
        font = label.font()
        font.setPointSize(30)
        label.setFont(font)
        self.label = label
        btn = QPushButton("벤처기업 검색")
        btn.clicked.connect(self.onButtonClicked)
        layout.addWidget(label)
        layout.addWidget(btn)
        layout.addStretch(1)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def onButtonClicked(self):
        self.win = Window()
        r = self.win.showModal()
        if r:
            text = self.win.edit.text()
            self.label.setText(text)
    def show(self):
        super().show()
