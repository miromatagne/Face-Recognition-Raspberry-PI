import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.camera import Camera
from kivy.lang import Builder
import cv2
import face_recognition
import os
import numpy as np
import faces

path = '/home/pi/Desktop/proj-h402-face-recognition/testImages'
fileList = os.listdir(path)
images = []

for f in fileList:
    currentImg = cv2.imread(path + "/" + f)
    images.append(currentImg)


def find_encodings(images):
    encodings = []
    for im in images:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(im)[0]
        encodings.append(encode)
    return encodings

print(len(images))
knownEncodings = find_encodings(images)
print(knownEncodings)

class MainWindow(Screen):
    def printPixels(self,cam):
        while True:
            frame = np.frombuffer(cam.texture.pixels,np.uint8)
            frame = frame.reshape((cam.texture.size[1],cam.texture.size[0],4))
            resizedImage = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            resizedImage = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2RGB)
            webcamFaces = face_recognition.face_locations(resizedImage)
            webcamEncoding = face_recognition.face_encodings(resizedImage, webcamFaces)

            for encodedFace, faceLocation in zip(webcamEncoding, webcamFaces):
                print("OK1")
                matches = face_recognition.compare_faces(knownEncodings, encodedFace)
                faceDistances = face_recognition.face_distance(knownEncodings, encodedFace)       
                matchId = np.argmin(faceDistances)

                if matches[matchId]:
                    name = fileList[matchId]
                    print(name)

class SecondWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("ui.kv")

class Program(App):
    def build(self):
        return kv


if __name__ == "__main__":
    Program().run()
