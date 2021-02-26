import kivy
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
from kivy.lang import Builder
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
  
docs = get_documents()
knownEncodings = []
users = []
for d in docs:
    knownEncodings.append(d["encoding"])
    users.append({"_id":str(d["_id"]),"name":d["firstName"],"telehpone":d["telephone"],"email":d["email"]})

values = get_sheet_content()

"""
for i in range(500,5000):
    encoding = np.random.uniform(low=-1,high=1,size=(128,))
    new_user_id = post_to_db("Miro" + str(i),"Test","21/03/2000","0467534184","mirotest@gmail.com","black",encoding.tolist())
    add_user("Miro" + str(i),"Test","21/03/2000","0467534184","mirotest@gmail.com","black",new_user_id)
    if i % 55 == 0:
        time.sleep(61)
"""

class MainWindow(Screen):
    def __init__(self,cam,**kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.name = "Main"
        grid = GridLayout(cols=1)
        self.img = Image(pos_hint={'center_x': 0.5, 'center_y': 0.5})
        grid.add_widget(self.img)
        subgrid = GridLayout(cols=3)
        registerButton = Button(text="Register",size_hint_y=None,height='48dp')
        guestButton = Button(text="Guest",size_hint_y=None,height='48dp')
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
        frame,recognizedUsers = get_matches(frame,knownEncodings,users)
        
        if len(recognizedUsers) != 0 and not self.popupIsOpen:
            popupText = "Welcome "
            for n in recognizedUsers:
                popupText += n["name"] + ' '
            popupText += '!'
            self.popup.content = Label(text=popupText)
            self.popupIsOpen = True
            self.popup.open()
            for n in recognizedUsers:
                write_presence(values,n["_id"])
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


class RegisterInfoWindow(Screen):
    def __init__(self,**kwargs):
        super(RegisterInfoWindow, self).__init__(**kwargs)
        self.name = "RegisterInfo"
        grid = GridLayout(cols=2)
        
        #First name
        firstNameLabel = Label(text="First name :")
        self.firstNameInput=TextInput(multiline=False)
        grid.add_widget(firstNameLabel)
        grid.add_widget(self.firstNameInput)
        
        #Last name
        lastNameLabel = Label(text="Last name :")
        self.lastNameInput=TextInput(multiline=False)
        grid.add_widget(lastNameLabel)
        grid.add_widget(self.lastNameInput)
        
        #Date of birth
        dobLabel = Label(text="Date of Birth :")
        self.dobInput=TextInput(multiline=False)
        grid.add_widget(dobLabel)
        grid.add_widget(self.dobInput)
        
        #Telephone
        telephoneLabel = Label(text="Telephone :")
        self.telephoneInput=TextInput(multiline=False)
        grid.add_widget(telephoneLabel)
        grid.add_widget(self.telephoneInput)
        
        #Email
        emailLabel = Label(text="Email :")
        self.emailInput=TextInput(multiline=False)
        grid.add_widget(emailLabel)
        grid.add_widget(self.emailInput)
        
        #Belt
        beltLabel = Label(text="Belt :")
        self.beltDropdown = DropDown()
        ranks = ["white","blue","purple","brown","black"]
        for i in range(len(ranks)):
            btn = Button(text=ranks[i], size_hint_y=None, height=44,on_release=lambda btn: self.beltDropdown.select(btn.text))
            self.beltDropdown.add_widget(btn)
        self.beltButton = Button(text="Belt rank",size_hint=(None, None))
        self.beltButton.bind(on_release=self.beltDropdown.open)
        self.beltDropdown.bind(on_select=lambda instance, x: setattr(self.beltButton, 'text', x))
        grid.add_widget(beltLabel)
        grid.add_widget(self.beltButton)
        
        confirmButton = Button(text="Confirm",size_hint_y=None,height='48dp')
        cancelButton = Button(text="Cancel",size_hint_y=None,height='48dp')
        confirmButton.bind(on_press=lambda x:self.switch_screen(self,"RegisterPhoto"))
        cancelButton.bind(on_press=lambda x:print(self.beltButton.text))
        grid.add_widget(confirmButton)
        grid.add_widget(cancelButton)
        
        self.add_widget(grid)
        
    def switch_screen(self,instance,screen):
        self.parent.current = screen


class RegisterPhotoWindow(Screen):
    def __init__(self,cam,**kwargs):
        super(RegisterPhotoWindow, self).__init__(**kwargs)
        self.name = "RegisterPhoto"
        grid = GridLayout(cols=1)
        self.img = Image(pos_hint={'center_x': 0.5, 'center_y': 0.5})
        grid.add_widget(self.img)
        subgrid = GridLayout(cols=3)
        cancelButton = Button(text="Cancel",size_hint_y=None,height='48dp')
        cancelButton.bind(on_press=lambda x:self.switch_screen(self,"RegisterInfo"))
        photoButton = Button(text="Go",size_hint_y=None,height='48dp')
        photoButton.bind(on_press=self.start_capture)
        self.countdownText = Label(text="5")
        subgrid.add_widget(self.countdownText)
        subgrid.add_widget(cancelButton)
        subgrid.add_widget(photoButton)
        grid.add_widget(subgrid)
        self.add_widget(grid)
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
        frame,encodings = get_faces_frame(frame)
        if(self.countdownText.text.isnumeric() and int(self.countdownText.text) == 0):
            self.countdownText.text = "Done !"
            if(len(encodings) > 0):
                new_user_id = post_to_db(self.parent.get_screen("RegisterInfo").firstNameInput.text,self.parent.get_screen("RegisterInfo").lastNameInput.text,self.parent.get_screen("RegisterInfo").dobInput.text,self.parent.get_screen("RegisterInfo").telephoneInput.text,self.parent.get_screen("RegisterInfo").emailInput.text,self.parent.get_screen("RegisterInfo").beltButton.text,encodings[0].tolist())
                add_user(self.parent.get_screen("RegisterInfo").firstNameInput.text,self.parent.get_screen("RegisterInfo").lastNameInput.text,self.parent.get_screen("RegisterInfo").dobInput.text,self.parent.get_screen("RegisterInfo").telephoneInput.text,self.parent.get_screen("RegisterInfo").emailInput.text,self.parent.get_screen("RegisterInfo").beltButton.text,new_user_id)
            else:
                print("No face")
            
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
        

class ProblemWindow(Screen):
    def __init__(self,**kwargs):
        super(ProblemWindow, self).__init__(**kwargs)
        self.name = "Problem"
        grid = GridLayout(cols=2)
        
        #First name
        firstNameLabel = Label(text="First name :")
        self.firstNameInput=TextInput(multiline=False)
        grid.add_widget(firstNameLabel)
        grid.add_widget(self.firstNameInput)
        
        #Last name
        lastNameLabel = Label(text="Last name :")
        self.lastNameInput=TextInput(multiline=False)
        grid.add_widget(lastNameLabel)
        grid.add_widget(self.lastNameInput)
        
        confirmButton = Button(text="Confirm",size_hint_y=None,height='48dp')
        cancelButton = Button(text="Cancel",size_hint_y=None,height='48dp')
        confirmButton.bind(on_press=lambda x:write_presence_from_name(values,self.firstNameInput.text,self.lastNameInput.text))
        cancelButton.bind(on_press=lambda x:self.switch_screen(self,"Main"))
        grid.add_widget(confirmButton)
        grid.add_widget(cancelButton)
        
        self.add_widget(grid)
        
    def switch_screen(self,instance,screen):
        self.parent.current = screen
        

class AlreadyMemberWindow(Screen):
    def __init__(self,**kwargs):
        super(AlreadyMemberWindow, self).__init__(**kwargs)
        self.name = "AlreadyMember"
        self.grid = GridLayout(cols=2)
        
        #First name
        nameLabel = Label(text="Name :")
        self.nameInput=TextInput(multiline=False)
        self.nameInput.bind(text=lambda x,y:self.update_list(self))
        self.grid.add_widget(nameLabel)
        self.grid.add_widget(self.nameInput)

        
        confirmButton = Button(text="Confirm",size_hint_y=None,height='48dp')
        cancelButton = Button(text="Cancel",size_hint_y=None,height='48dp')
        confirmButton.bind(on_press=lambda x:self.update_list(self))
        cancelButton.bind(on_press=lambda x:self.switch_screen(self,"Main"))
        
        self.listScroll = ScrollView(size_hint=(1,1))
        self.grid.add_widget(self.listScroll)
        
        self.grid.add_widget(confirmButton)
        self.grid.add_widget(cancelButton)
        
        self.add_widget(self.grid)
    
    def update_list(self,instance):
        self.listScroll.clear_widgets()
        listGrid = GridLayout(cols=1,spacing=10,size_hint_y=None)
        listGrid.bind(minimum_height=listGrid.setter('height'))
        for i in range(len(values)):
            name = values[i][0] + " " + values[i][1]
            if self.nameInput.text != "" and self.nameInput.text in name:
                listGrid.add_widget(Label(text=name))
        self.listScroll.add_widget(listGrid)
        
    def switch_screen(self,instance,screen):
        self.parent.current = screen
        

class Program(App):
    def build(self):
        self.cam = Camera(play=True)
        sm = ScreenManager()
        sm.add_widget(MainWindow(self.cam))
        sm.add_widget(RegisterInfoWindow())
        sm.add_widget(RegisterPhotoWindow(self.cam))
        sm.add_widget(ProblemWindow())
        sm.add_widget(AlreadyMemberWindow())
        return sm


if __name__ == "__main__":
    Program().run()
