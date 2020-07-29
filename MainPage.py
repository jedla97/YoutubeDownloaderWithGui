import os
import sys
import re
import requests
from os.path import expanduser

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi

import App


# pyinstaller --onefile --icon=resources/icon.ico --clean MainPage.py

# testing if inputted url matched youtube arguments
def checkIfUrlMatchingParameters(url):
    ytReg = (r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{'
             r'11})')

    ytReg_result = re.match(ytReg, url)
    if ytReg_result:
        return True

    return False


# testing if url exist with testing on youtube url
def urlExists(url):
    if checkIfUrlMatchingParameters(url):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            return True
        else:
            return False
    else:
        return False


# check if file for last path exist if not create new
def checkIfFileExist(filePath):
    if not os.path.exists(filePath):
        open(filePath, "w").close


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
            self.setErrorVisible(100, "red")
            self.error.setText("Invalid input in url.\n")
            self.error.setAlignment(QtCore.Qt.AlignCenter)
            self.error.append("Invalid input in file name.")
            self.error.setAlignment(QtCore.Qt.AlignCenter)
            self.fileName.setStyleSheet("background-color: red;")
            self.url.setStyleSheet("background-color: red;")
        # only url is blank or non-existent show error and red mark the url input field
        elif url == "-1":
            self.setErrorVisible(50, "red")
            self.error.setText("Invalid input in url.")
            self.error.setAlignment(QtCore.Qt.AlignCenter)
            self.url.setStyleSheet("background-color: red;")
        # only fileName is blank show error and red mark the url input field
        elif fileName == "-1":
            self.setErrorVisible(50, "red")
            self.error.setText("Invalid input in file name.")
            self.error.setAlignment(QtCore.Qt.AlignCenter)
            self.fileName.setStyleSheet("background-color: red;")
        # both inputs are includes valid
        else:
            self.error.setVisible(False)
            path = ""
            # getting last path when app was used if first usage or path not existing redirect to desktop when not
            # file not exist function create nwe
            checkIfFileExist("resources\\LastPath.txt")
            try:
                f = open("resources\\LastPath.txt", "r")
                lastPath = f.readline()
                f.close()
            # when file not created by function program exits with -3
            except FileNotFoundError:
                print("Cannot open file check if place where you installed file for file LastPath.txt in "
                      "resources directory if missing create new one")
                exit(-3)
            # checking whats in lastFile.txt and if exist
            if lastPath != "" and os.path.isdir(lastPath):
                path = QFileDialog.getExistingDirectory(self, "select directory", lastPath,
                                                        QFileDialog.ShowDirsOnly)
            else:
                path = QFileDialog.getExistingDirectory(self, "select directory", expanduser("~") + "\Desktop",
                                                        QFileDialog.ShowDirsOnly)
            # when close save dialog return none and when path not exist show error message
            if not os.path.isdir(path):
                if path == "":
                    return None
                else:
                    self.errorHandling(self, -2)
            #  if user choose mp3 download as mp3 and the same for mp4 with different message after downloaded
            if self.fileType.currentText() == "MP3":
                file = App.Download(url, self.fileType.currentText(), path, fileName)
                self.fileWillBeDownload(fileName)
                QApplication.processEvents()
                errorCode = file.downloadAsMp3()
                if errorCode == -4 or errorCode == -5 or errorCode == -6:
                    self.errorHandling(errorCode)
                else:
                    self.fileDownloaded(fileName, path, "MP3")
            elif self.fileType.currentText() == "MP4":
                file = App.Download(url, self.fileType.currentText(), path, fileName)
                self.error.setAlignment(QtCore.Qt.AlignCenter)
                self.fileWillBeDownload(fileName)
                QApplication.processEvents()
                if file.downloadAsMp4() != -4:
                    self.fileDownloaded(fileName, path, "MP4")
                else:
                    self.errorHandling(-4)
            else:
                print("error")
            # saving path for next usage when downloaded(lastPath for usage)
            checkIfFileExist("resources\\LastPath.txt")
            try:
                f = open("resources\\LastPath.txt", "w")
                f.write(path)
                f.close()
            except Exception as e:
                print("something goes wrong".format(e))
                exit(-3)

    # error handling function by return negative numbers for description see error text
    def errorHandling(self, errorID):
        if errorID == -2:
            self.setErrorVisible(50, "red")
            self.error.setText("Not existing Path to directory")
        elif errorID == -3:
            self.setErrorVisible(150, "red")
            self.error.setText("Cannot open file check if place where you installed file for file LastPath.txt in "
                               "resources directory if missing create new one")
        elif errorID == -4:
            self.setErrorVisible(50, "red")
            self.error.setText("Video cannot be downloaded check it's availability")
        elif errorID == -5:
            self.setErrorVisible(100, "red")
            self.error.setText("MP4 video cannot be deleted because some problems delete manually sorry for "
                               "inconvenience")
        elif errorID == -6:
            self.setErrorVisible(100, "red")
            self.error.setText("Video cannot be converted try again when fail again contact administrator")
        else:
            self.setErrorVisible(50, "red")
            self.error.setText("Not know error code contact your administrator")
        self.error.setAlignment(QtCore.Qt.AlignCenter)

    # set error placeholder visible and set high and background color
    def setErrorVisible(self, high, color):
        self.error.setVisible(True)
        self.error.resize(600, high)
        self.error.setStyleSheet("background-color: " + color + "; font-weight: bold; font-size: 16pt;")

    # set message when downloading start
    def fileWillBeDownload(self, name):
        self.setErrorVisible(50, "white")
        self.error.setText("Video " + name + " is downloading")
        self.error.setAlignment(QtCore.Qt.AlignCenter)

    # set text after successfully downloaded
    def fileDownloaded(self, name, path, fileFormat):
        self.setErrorVisible(100, "green")
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
