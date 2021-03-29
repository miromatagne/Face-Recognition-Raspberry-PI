import os
#os.environ['KIVY_AUDIO'] = 'sdl2'
import kivy
import info
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.camera import Camera
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
import cv2
import face_recognition
from picamera import PiCamera
import os
import pickle
import numpy as np
from faces import find_encodings,get_matches,get_faces_frame
from database import post_to_db,get_documents
from participant_list import add_user,get_sheet_content,write_presence,write_presence_from_name
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
import time

from main_window import MainWindow
from register_info_window import RegisterInfoWindow
from register_photo_window import RegisterPhotoWindow
from already_member_window import AlreadyMemberWindow
from already_member_photo_window import AlreadyMemberPhotoWindow
from problem_window import ProblemWindow

"""
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
"""
"""  
docs = get_documents()
knownEncodings = []
users = []
for d in docs:
    knownEncodings.append(d["encoding"])
    users.append({"_id":str(d["_id"]),"name":d["firstName"],"telehpone":d["telephone"],"email":d["email"]})

values = get_sheet_content()
"""
"""
for i in range(500,5000):
    encoding = np.random.uniform(low=-1,high=1,size=(128,))
    new_user_id = post_to_db("Miro" + str(i),"Test","21/03/2000","0467534184","mirotest@gmail.com","black",encoding.tolist())
    add_user("Miro" + str(i),"Test","21/03/2000","0467534184","mirotest@gmail.com","black",new_user_id)
    if i % 55 == 0:
        time.sleep(61)
"""
          
class Program(App):
    def build(self):
        self.cam = Camera(play=True)
        sm = ScreenManager()
        sm.add_widget(MainWindow(self.cam))
        sm.add_widget(RegisterInfoWindow())
        sm.add_widget(RegisterPhotoWindow(self.cam))
        sm.add_widget(ProblemWindow())
        sm.add_widget(AlreadyMemberWindow())
        sm.add_widget(AlreadyMemberPhotoWindow(self.cam))
        return sm
    

if __name__ == "__main__":
    Window.fullscreen = 'auto'
    Window.clearcolor = (1, 1, 1, 1)
    info.init()
    Program().run()
