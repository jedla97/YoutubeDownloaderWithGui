import os
import sys
from os.path import expanduser

import requests
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi

import App


# testing if inputted url include youtube url
def urlInclude(url):
    youtubeUrl = ["https://www.youtube.com/", "www.youtube.com/", "youtube.com/", "https://youtube.com/"]
    for i in youtubeUrl:
        if i in url:
            return True
    return False


# testing if url exist with testing on youtube url
def urlExists(url):
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
        self.error.setVisible(False)  # error window set to non visible
        self.down.clicked.connect(self.download)
        self.url.setPlaceholderText("write url of youtube video like \"https://www.youtube.com/watch?v=jhl5afLEKdo\"")
        self.fileName.setPlaceholderText("write the name under which the file should be saved")

    def download(self):
        self.setToNoColor()
        path = ""
        url = self.getUrl()
        fileName = self.getNameOfFile()
        # url and fileName is blank or url is non-existent show error and red mark the blank input field
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
        # only url is blank or non-existent show error and red mark the url input field
        elif url == "-1":
            self.error.setVisible(True)
            self.error.resize(600, 50)
            self.error.setStyleSheet("background-color: red; font-weight: bold; font-size: 16pt;")
            self.error.setText("Invalid input in url.")
            self.error.setAlignment(QtCore.Qt.AlignCenter)
            self.url.setStyleSheet("background-color: red;")
        # only fileName is blank show error and red mark the url input field
        elif fileName == "-1":
            self.error.setVisible(True)
            self.error.resize(600, 50)
            self.error.setStyleSheet("background-color: red; font-weight: bold; font-size: 16pt;")
            self.error.setText("Invalid input in file name.")
            self.error.setAlignment(QtCore.Qt.AlignCenter)
            self.fileName.setStyleSheet("background-color: red;")
        # both inputs are includes valid
        else:
            self.error.setVisible(False)
            # getting last path when app was used if first usage or path not existing redirect to desktop
            try:
                f = open("resources\\LastPath.txt", "r")
                lastPath = f.readline()
                f.close()
            except Exception as e:
                print("something goes wrong".format(e))
                exit(-3)
            if lastPath != "" and os.path.isdir(lastPath):
                path = QFileDialog.getExistingDirectory(self, "select directory", lastPath,
                                                        QFileDialog.ShowDirsOnly)
            else:
                path = QFileDialog.getExistingDirectory(self, "select directory", expanduser("~") + "\Desktop",
                                                        QFileDialog.ShowDirsOnly)
            if not os.path.isdir(path):
                exit(-2)
            #  if user choose mp3 download as mp3 and the same for mp4 with different message after downloaded
            if self.fileType.currentText() == "MP3":
                file = App.Download(url, self.fileType.currentText(), path, fileName)
                file.downloadAsMp3()
                self.fileDownloaded(fileName, path, "MP3")
            elif self.fileType.currentText() == "MP4":
                file = App.Download(url, self.fileType.currentText(), path, fileName)
                self.error.setAlignment(QtCore.Qt.AlignCenter)
                file.downloadAsMp4()
                self.fileDownloaded(fileName, path, "MP4")
            else:
                print("error")
            # saving path for next usage when downloaded(lastPath for usage)
            try:
                f = open("resources\\LastPath.txt", "w")
                f.write(path)
                f.close()
            except Exception as e:
                print("something goes wrong".format(e))
                exit(-3)

    # set text after successfully downloaded
    def fileDownloaded(self, name, path, fileFormat):
        self.error.setVisible(True)
        self.error.resize(600, 100)
        self.error.resize(600, 100)
        self.error.setStyleSheet("font-weight: bold; font-size: 16pt;")
        if fileFormat == "MP3":
            self.error.setText("Video " + name + ".mp3 was saved to " + path)
        elif fileFormat == "MP4":
            self.error.setText("Video " + name + ".mp4 was saved to " + path)
        else:
            self.error.setStyleSheet("background-color: red; font-weight: bold; font-size: 16pt;")
            self.error.setText("something goes wrong in printing download status")
        self.error.setAlignment(QtCore.Qt.AlignCenter)

    # setting color to default after invalid input for next testing input
    def setToNoColor(self):
        self.url.setStyleSheet("background-color: none;")
        self.fileName.setStyleSheet("background-color: none;")

    # getting url from input field
    def getUrl(self):
        url = self.url.text()
        # testing if url exists
        if urlExists(url):
            return url
        else:
            return "-1"

    # getting name of file for save
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
