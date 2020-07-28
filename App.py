from moviepy import video
from pytube import YouTube as Yt
from moviepy.video.io.VideoFileClip import VideoFileClip
import os


# check if file exist
def checkIfFileExist(filePath):
    if not os.path.exists(filePath):
        return False
    else:
        return True


class Download:
    def __init__(self, urlSource, typeOfFile, savePath, fileName):
        self.urlSource = urlSource
        self.typeOfFile = typeOfFile
        self.savePath = savePath
        self.fileName = fileName

    # download mp4 video via pytube, convert to mp3  and delete mp4
    def downloadAsMp3(self):
        # try download video when cannot return error code
        try:
            ytd = Yt(self.urlSource)  # creating object of video
            ytd.streams.get_lowest_resolution().download(self.savePath, self.fileName)  # download mp4
            # try convert video when cannot return error code
            try:
                self.convertToMp3()  # convert mp4
                # removing mp4
                if checkIfFileExist(self.savePath + "/" + self.fileName + ".mp4"):
                    # try remove video when cannot return error code
                    try:
                        os.remove(self.savePath + "/" + self.fileName + ".mp4")
                    finally:
                        if not checkIfFileExist(self.savePath + "/" + self.fileName + ".mp4"):
                            return -5
            finally:
                if not checkIfFileExist(self.savePath + "/" + self.fileName + ".mp3"):
                    return -6
        finally:
            if not checkIfFileExist(self.savePath + "/" + self.fileName + ".mp3"):
                return -4

    # convert mp4 to mp3 via moviepy
    def convertToMp3(self):
        videoClip = VideoFileClip(self.savePath + "/" + self.fileName + ".mp4")
        audioClip = videoClip.audio
        audioClip.write_audiofile(self.savePath + "/" + self.fileName + ".mp3")
        audioClip.close()
        videoClip.close()

    # download mp4 via pytube
    def downloadAsMp4(self):
        # try download video when cannot return error code
        try:
            ytd = Yt(self.urlSource)  # creating object of video
            ytd.streams.get_highest_resolution().download(self.savePath, self.fileName)  # download mp4
        finally:
            if not checkIfFileExist(self.savePath + "/" + self.fileName + ".mp4"):
                return -4


'''
# for testing purpose when some vid bad download print all and download by id(itag)
vid = Yt('url')
for x in vid.streams:
    print(x)
print("\n")
print(vid.streams.get_highest_resolution())
vid.streams.get_by_itag(22).download('location', "name")
'''
