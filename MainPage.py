import os
import sys
from os.path import expanduser

import requests
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi

import App


def urlInclude(url):
    youtubeUrl = ["https://www.youtube.com/", "www.youtube.com/", "youtube.com/", "https://youtube.com/"]
    for i in youtubeUrl:
        if i in url:
            return True
    return False


def uriExists(url):
    if urlInclude(url):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            return True
        else:
            return False
    else:
        return False


class MainPage(QMainWindow):
    def __init__(self):
        super(MainPage, self).__init__()
        loadUi('resources\\mainwindow.ui', self)
        self.error.setVisible(False)
        self.down.clicked.connect(self.download)
        self.url.setPlaceholderText("write url of youtube video like \"https://www.youtube.com/watch?v=jhl5afLEKdo\"")
        self.fileName.setPlaceholderText("write the name under which the file should be saved")

    def download(self):
        self.setToNoColor()
        path = ""
        url = self.getUrl()
        fileName = self.getNameOfFile()
        if url == "-1" and fileName == "-1":
            self.error.setVisible(True)
            self.error.resize(600, 120)
            self.error.setStyleSheet("background-color: red; font-weight: bold; font-size: 16pt;")
            self.error.setText("Invalid input in url.\n")
            self.error.setAlignment(QtCore.Qt.AlignCenter)
            self.error.append("Invalid input in file name.")
            self.error.setAlignment(QtCore.Qt.AlignCenter)
            self.fileName.setStyleSheet("background-color: red;")
            self.url.setStyleSheet("background-color: red;")
        elif url == "-1":
            self.error.setVisible(True)
            self.error.resize(600, 50)
            self.error.setStyleSheet("background-color: red; font-weight: bold; font-size: 16pt;")
            self.error.setText("Invalid input in url.")
            self.error.setAlignment(QtCore.Qt.AlignCenter)
            self.url.setStyleSheet("background-color: red;")
        elif fileName == "-1":
            self.error.setVisible(True)
            self.error.resize(600, 50)
            self.error.setStyleSheet("background-color: red; font-weight: bold; font-size: 16pt;")
            self.error.append("Invalid input in file name.")
            self.error.setAlignment(QtCore.Qt.AlignCenter)
            self.fileName.setStyleSheet("background-color: red;")
        else:
            self.error.setVisible(False)
            try:
                f = open("resources\\LastPath.txt", "r")
                lastPath = f.readline()
                f.close()
            except Exception as e:
                print("something goes wrong".format(e))
                exit(-3)
            if lastPath != "":
                path = QFileDialog.getExistingDirectory(self, "select directory", lastPath,
                                                        QFileDialog.ShowDirsOnly)
            else:
                path = QFileDialog.getExistingDirectory(self, "select directory", expanduser("~") + "\Desktop",
                                                        QFileDialog.ShowDirsOnly)
            if not os.path.isdir(path):
                exit(-2)
            if self.fileType.currentText() == "MP3":
                file = App.Download(url, self.fileType.currentText(), path, fileName)
                file.downloadAsMp3()
                self.fileDownloaded(fileName, url, "MP3")
            elif self.fileType.currentText() == "MP4":
                file = App.Download(url, self.fileType.currentText(), path, fileName)
                self.error.setAlignment(QtCore.Qt.AlignCenter)
                file.downloadAsMp4()
                self.fileDownloaded(fileName, url, "MP4")
            else:
                print("error")
            try:
                f = open("resources\\LastPath.txt", "w")
                f.write(path)
                f.close()
            except Exception as e:
                print("something goes wrong".format(e))
                exit(-3)

    def fileDownloaded(self, name, url, fileFormat):
        self.error.setVisible(True)
        self.error.resize(600, 100)
        self.error.resize(600, 100)
        self.error.setStyleSheet("font-weight: bold; font-size: 16pt;")
        if fileFormat == "MP3":
            self.error.append("Video " + name + ".mp3 was downloaded from " + url)
        elif fileFormat == "MP4":
            self.error.append("Video " + name + ".mp4 was downloaded from " + url)
        else:
            self.error.append("something goes wrong in printing download status")
        self.error.setAlignment(QtCore.Qt.AlignCenter)

    def setToNoColor(self):
        self.url.setStyleSheet("background-color: none;")
        self.fileName.setStyleSheet("background-color: none;")

    def getUrl(self):
        url = self.url.text()
        if uriExists(url):
            return url
        else:
            return "-1"

    def getNameOfFile(self):
        name = self.fileName.text()
        if name != "":
            return name
        else:
            return "-1"


# this is for show gui
app = QApplication(sys.argv)
widget = MainPage()
widget.show()
sys.exit(app.exec_())
