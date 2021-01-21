import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.lang import Builder
import cv2
import face_recognition
from picamera import PiCamera
import os
import pickle
import numpy as np
from faces import find_encodings,get_matches
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window

data = pickle.loads(open("encodings.pickle", "rb").read())
names = data["names"]
knownEncodings = data["encodings"]


path = '/home/pi/Desktop/proj-h402-face-recognition/testImages'
fileList = os.listdir(path)
newImages = []
newNames = []

for f in fileList:
    if(f not in names):
        currentImg = cv2.imread(path + "/" + f)
        newImages.append(currentImg)
        newNames.append(f)

if len(newImages) != 0:
    newEncodings = find_encodings(newImages)
    for e,n in zip(newEncodings,newNames):
        knownEncodings.append(e)
        names.append(n)

    data = {"encodings": knownEncodings,"names": names}
    f = open("encodings.pickle", "wb")
    f.write(pickle.dumps(data))
    f.close()


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
        self.popup = Popup(title='Welcome !',content=Label(text='Hello world'),auto_dismiss=False,size_hint=(.8, .8))
        self.popupIsOpen = False
        self.cam = Camera(play=True)
        Clock.schedule_interval(self.update_texture, 1.0 / 60.0)
    
    def update_texture(self,instance):
        """
            Updates the live camera stream and calls the face recognition
            functions. Draws squares around recognized faces and opens
            the popup when a face has been recognized.
        """
        frame = np.frombuffer(self.cam.texture.pixels,np.uint8)
        frame = frame.reshape((self.cam.texture.size[1],self.cam.texture.size[0],4))
        frame,names = get_matches(frame,knownEncodings,fileList)
        
        if len(names) != 0 and not self.popupIsOpen:
            popupText = "Welcome "
            for n in names:
                popupText += n + ' '
            popupText += '!'
            self.popup.content = Label(text=popupText)
            self.popupIsOpen = True
            self.popup.open()
            Clock.schedule_once(self.close_popup, 2)
        
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
        
    def close_popup(self,instance):
        """
            Closes the popup
        """
        self.popup.dismiss()
        self.popupIsOpen = False


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
