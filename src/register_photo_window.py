import kivy
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from faces import get_faces_frame
from database import post_to_db
from participant_list import add_user
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from database import post_to_db,get_documents
from participant_list import add_user,get_sheet_content,write_presence,write_presence_from_name
import numpy as np
import cv2
import time
from custom_button import CustomButton


class RegisterPhotoWindow(Screen):
    def __init__(self,cam,**kwargs):
        super(RegisterPhotoWindow, self).__init__(**kwargs)
        self.name = "RegisterPhoto"
        grid = GridLayout(cols=1)
        self.img = Image(size_hint_y=10)
        grid.add_widget(self.img)
        self.info_label = Label(text="Press the confirm button, a picture of you will be taken in 5 seconds. Make sure your face is clearly visible !")
        grid.add_widget(self.info_label)
        subgrid = GridLayout(cols=3,size_hint_y=1)
        cancelButton = CustomButton(text="Cancel")
        cancelButton.bind(on_press=lambda x:self.switch_screen(self,"RegisterInfo"))
        photoButton = CustomButton(text="Go")
        photoButton.bind(on_press=self.start_capture)
        self.countdownText = Label(text="5")
        subgrid.add_widget(self.countdownText)
        subgrid.add_widget(cancelButton)
        subgrid.add_widget(photoButton)
        grid.add_widget(subgrid)
        self.add_widget(grid)
        self.cam = cam
        Clock.schedule_interval(self.update_texture, 1.0 / 100.0)
        
        
    def update_texture(self,instance):
        """
            Updates the live camera stream and calls the face recognition
            functions. Draws squares around recognized faces and opens
            the popup when a face has been recognized.
        """
            
        frame = np.frombuffer(self.cam.texture.pixels,np.uint8)
        frame = frame.reshape((self.cam.texture.size[1],self.cam.texture.size[0],4))
        frame,encodings = get_faces_frame(frame)
        if(self.countdownText.text.isnumeric() and int(self.countdownText.text) == 0):
            self.countdownText.text = "Done !"
            if(len(encodings) > 0):
                self.info_label.text = "Your registration was successful, you will be redirected towards the main screen."
                new_user_id = post_to_db(self.parent.get_screen("RegisterInfo").firstNameInput.text,self.parent.get_screen("RegisterInfo").lastNameInput.text,self.parent.get_screen("RegisterInfo").dobInput.text,self.parent.get_screen("RegisterInfo").telephoneInput.text,self.parent.get_screen("RegisterInfo").emailInput.text,self.parent.get_screen("RegisterInfo").beltButton.text,encodings[0].tolist())
                add_user(self.parent.get_screen("RegisterInfo").firstNameInput.text,self.parent.get_screen("RegisterInfo").lastNameInput.text,self.parent.get_screen("RegisterInfo").dobInput.text,self.parent.get_screen("RegisterInfo").telephoneInput.text,self.parent.get_screen("RegisterInfo").emailInput.text,self.parent.get_screen("RegisterInfo").beltButton.text,new_user_id)
                Clock.schedule_once(lambda x : self.switch_screen(self,"Main"),2.0)
            else:
                self.countdownText.text = "5"
                self.info_label.text = "Your face was not recognized, please try again"
            
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
        
    def decrement_countdown(self,instance):
        self.countdownText.text = str(int(self.countdownText.text) - 1)
        
    def start_capture(self,instance):
        Clock.schedule_once(self.decrement_countdown,1)
        Clock.schedule_once(self.decrement_countdown,2)
        Clock.schedule_once(self.decrement_countdown,3)
        Clock.schedule_once(self.decrement_countdown,4)
        Clock.schedule_once(self.decrement_countdown,5)
        
    def switch_screen(self,instance,screen):
        if screen == "Main":
            Clock.schedule_interval(self.parent.get_screen('Main').update_texture, 1.0 / 60.0)
        self.parent.current = screen