# Author: Jimmy Palomino
# email: jimmy.palomino@yahoo.com, jimspalo@espol.edu.ec
# linkedIn: https://www.linkedin.com/in/jimmypalomino/

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMenu
from PyQt5.QtCore import QEvent
import sys
import requests
import random
from PyQt5.QtCore import QTimer, QTime, QDate


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self._initUI()

    def _initUI(self):
        self.setGeometry(430, 410, 800, 600)
        self.setWindowTitle('Postulante para ROBOTILSA S.A')
        self.setMinimumSize(QtCore.QSize(800, 600))
        self.setMaximumSize(QtCore.QSize(800, 600))

        self._request_buttom()
        self._labelDate()
        self._labelTime()
        self._list()
        self._updateItem()

        timer = QTimer(self)
        timer.timeout.connect(self._updateTime)
        timer.timeout.connect(self._updateDate)
        timer.start(1000)

    def _request_buttom(self):
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(430, 410, 161, 61))
        self.pushButton.setText("Request")
        self.pushButton.clicked.connect(self._updateItem)

    def _labelDate(self):
        self.labelDate = QtWidgets.QLabel(self)
        self.labelDate.setGeometry(QtCore.QRect(440, 160, 161, 41))
        self.labelDate.setStyleSheet("font: 75 20pt \"Times New Roman\";")

    def _updateDate(self):
        currentDate = QDate.currentDate()
        self.labelDate.setText(currentDate.toString("dd/MM/yyyy"))

    def _labelTime(self):
        self.labelTime = QtWidgets.QLabel(self)
        self.labelTime.setGeometry(QtCore.QRect(440, 250, 161, 41))
        self.labelTime.setStyleSheet("font: 75 20pt \"Times New Roman\";")

    def _updateTime(self):
        currentTime = QTime.currentTime()
        self.labelTime.setText(currentTime.toString("hh:mm:ss"))

    def _list(self):
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(30, 90, 256, 371))
        self.listWidget.setStyleSheet("font: 17pt \"Times New Roman\";")
        self.listWidget.setObjectName("listWidget")

        # Items
        for k in range(10):
            item = QtWidgets.QListWidgetItem()
            self.listWidget.addItem(item)

        self.listWidget.installEventFilter(self)

    def _updateItem(self):
        self.listWidget.setSortingEnabled(False)

        self.dataper = {}
        for k in range(10):
            a = random.choice(range(83))+1
            reply = requests.get("https://swapi.dev/api/people/"+str(a))
            datadic = reply.json()
            item = self.listWidget.item(k)
            item.setText(datadic['name'])
            self.dataper[datadic['name']] = datadic
            self.listWidget.doubleClicked

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.listWidget:

            menu = QMenu()
            menu.addAction("Información del personaje")

            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                self._popupwindows(item)

            return True

        return super().eventFilter(source, event)

    def _popupwindows(self, item):
        self.win = QMainWindow()
        self.win.resize(240, 320)
        self.win.setWindowTitle('Información del personaje')
        self.win.setMinimumSize(QtCore.QSize(240, 320))
        self.win.setMaximumSize(QtCore.QSize(240, 320))

        self.win.dic = self.dataper[item.text()]

        Data = ['height', 'mass', 'hair_color', 'skin_color',
                'eye_color', 'birth_year', 'gender']

        for k in range(7):
            self.win.labeltext = QtWidgets.QLabel(self.win)
            self.win.labeltext.setGeometry(QtCore.QRect(20, 10 + 40*k, 71, 16))
            self.win.labeltext.setStyleSheet(
                "font: 75 10pt \"Times New Roman\";")
            self.win.labeltext.setText(Data[k])

        for k in range(7):
            self.win.labeltext = QtWidgets.QLabel(self.win)
            self.win.labeltext.setGeometry(
                QtCore.QRect(110, 10 + 40*k, 71, 16))
            self.win.labeltext.setStyleSheet(
                "font: 75 10pt \"Times New Roman\";")
            self.win.labeltext.setText(self.win.dic[Data[k]])

        self.win.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
