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
