import os
os.environ['KIVY_AUDIO'] = 'sdl2'
import kivy
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
import cv2
import face_recognition
import numpy as np
from faces import find_encodings,get_matches,get_faces_frame
from database import post_to_db,get_documents
from participant_list import add_user,get_sheet_content,write_presence,write_presence_from_name
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
import info

class MainWindow(Screen):
    def __init__(self,cam,**kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.name = "Main"
        grid = GridLayout(cols=1)
        self.img = Image(size_hint_y=10)
        grid.add_widget(self.img)
        subgrid = GridLayout(cols=3,size_hint_y=1)
        registerButton = Button(text="Register",size_hint_y=None,height='48',background_color=(1,0,0,1))
        guestButton = Button(text="Guest",size_hint_y=None,height='48')
        alreadyMemberButton = Button(text="Already a member ?",size_hint_y=None,height='48dp')
        problemButton = Button(text="Problem ?",size_hint_y=None,height='48dp')
        registerButton.bind(on_press=lambda x:self.switch_screen(self,"RegisterInfo"))
        alreadyMemberButton.bind(on_press=lambda x:self.switch_screen(self,"AlreadyMember"))
        problemButton.bind(on_press=lambda x:self.switch_screen(self,"Problem"))
        subgrid.add_widget(registerButton)
        subgrid.add_widget(alreadyMemberButton)
        subgrid.add_widget(problemButton)
        grid.add_widget(subgrid)
        self.add_widget(grid)
        self.popup = Popup(title='Welcome !',content=Label(text='Hello world'),auto_dismiss=False,size_hint=(.8, .8))
        self.popupIsOpen = False
        self.cam = cam
        Clock.schedule_interval(self.update_texture, 1.0 / 60.0)
    
    def update_texture(self,instance):
        """
            Updates the live camera stream and calls the face recognition
            functions. Draws squares around recognized faces and opens
            the popup when a face has been recognized.
        """
        frame = np.frombuffer(self.cam.texture.pixels,np.uint8)
        frame = frame.reshape((self.cam.texture.size[1],self.cam.texture.size[0],4))
        frame,recognizedUsers = get_matches(frame,info.known_encodings,info.users)
        
        if len(recognizedUsers) != 0 and not self.popupIsOpen:
            popupText = "Welcome "
            for n in recognizedUsers:
                popupText += n["name"] + ' '
            popupText += '!'
            self.popup.content = Label(text=popupText)
            self.popupIsOpen = True
            self.popup.open()
            sound = SoundLoader.load('ding.wav')
            if sound:
                print("Sound found at %s" % sound.source)
                print("Sound is %.3f seconds" % sound.length)
                sound.play()
                sound.seek(0.00)
            for n in recognizedUsers:
                write_presence(info.values,n["_id"])
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
        
    def switch_screen(self,instance,screen):
        Clock.unschedule(self.update_texture)
        self.parent.current = screen
        