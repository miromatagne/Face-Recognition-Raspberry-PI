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
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from participant_list import write_presence_from_name
from kivy.clock import Clock
from custom_button import CustomButton


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
        
        confirmButton = CustomButton(text="Confirm")
        cancelButton = CustomButton(text="Cancel")
        confirmButton.bind(on_press=lambda x:write_presence_from_name(values,self.firstNameInput.text,self.lastNameInput.text))
        cancelButton.bind(on_press=lambda x:self.switch_screen(self,"Main"))
        grid.add_widget(confirmButton)
        grid.add_widget(cancelButton)
        
        self.add_widget(grid)
        
    def switch_screen(self,instance,screen):
        if screen == "Main":
            Clock.schedule_interval(self.parent.get_screen('Main').update_texture, 1.0 / 60.0)
        self.parent.current = screen