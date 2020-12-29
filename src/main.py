import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.lang import Builder
import cv2
import face_recognition
from picamera import PiCamera
import os
import numpy as np
import faces
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window


path = '/home/pi/Desktop/proj-h402-face-recognition/testImages'
fileList = os.listdir(path)
images = []

for f in fileList:
    currentImg = cv2.imread(path + "/" + f)
    images.append(currentImg)


def find_encodings(images):
    encodings = []
    for im in images:
        im = cv2.resize(im, (0, 0), None, 0.25, 0.25)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        encodeList = face_recognition.face_encodings(im)
        if(len(encodeList) != 0):
            encode = encodeList[0]
        encodings.append(encode)
    return encodings

print(len(images))
knownEncodings = find_encodings(images)
print(knownEncodings)


class MainWindow(Screen):
    def __init__(self,**kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.name = "Main"
        grid = GridLayout(cols=1)
        self.img = Image(pos_hint={'center_x': 0.5, 'center_y': 0.5})
        grid.add_widget(self.img)
        subgrid = GridLayout(cols=3)
        registerButton = Button(text="Register",size_hint_y=None,height='48dp')
        guestButton = Button(text="Guest",size_hint_y=None,height='48dp')
        problemButton = Button(text="Problem ?",size_hint_y=None,height='48dp')
        registerButton.bind(on_press=lambda x:print("OK"))
        guestButton.bind(on_press=lambda x:print("OK"))
        problemButton.bind(on_press=lambda x:print("OK"))
        subgrid.add_widget(registerButton)
        subgrid.add_widget(guestButton)
        subgrid.add_widget(problemButton)
        grid.add_widget(subgrid)
        self.add_widget(grid)
        
        self.cam = Camera(play=True)
        
        Clock.schedule_interval(self.update_texture, 1.0 / 60.0)
    
    def update_texture(self,instance):
        frame = np.frombuffer(self.cam.texture.pixels,np.uint8)
        frame = frame.reshape((self.cam.texture.size[1],self.cam.texture.size[0],4))
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
                y1, x2, y2, x1 = faceLocation
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,255,255), 4)
                cv2.rectangle(frame, (x1, y2-35), (x2, y2), (0, 0, 255,255), cv2.FILLED)
                cv2.putText(img=frame, text=name.split(".")[0], org=(x1+6, y2-6),fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=1, color=[255,255,255,255], lineType=cv2.LINE_AA, thickness=2)
                
        window_shape = Window.size
        window_width = window_shape[0]
        window_height = window_shape[1]
        frame = cv2.resize(frame, (int(window_height * (self.cam.texture.size[0]/self.cam.texture.size[1])), window_height))
        frame = frame.reshape((frame.shape[1],frame.shape[0], 4))
        buf = frame.tobytes()
        texture = Texture.create(size=(frame.shape[0], frame.shape[1]), colorfmt='rgba')
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()
        self.img.texture = texture


class SecondWindow(Screen):
    pass



class Program(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainWindow())
        sm.add_widget(SecondWindow())
        return sm


if __name__ == "__main__":
    Program().run()
