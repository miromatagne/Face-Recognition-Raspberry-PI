import os
#os.environ['KIVY_AUDIO'] = 'sdl2'
import kivy
import info
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
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
from custom_label import CustomLabel
from custom_textinput import CustomTextInput


class ProblemWindow(Screen):
    def __init__(self,**kwargs):
        super(ProblemWindow, self).__init__(**kwargs)
        self.name = "Problem"
        box = BoxLayout(spacing=20,orientation="vertical",padding=[20,0,20,0])
        grid = GridLayout(cols=2,padding=[0,100,0,0],size_hint_y=10)
        
        #First name
        firstNameGrid = GridLayout(cols=1)
        firstNameLabel = CustomLabel(text="First name :")
        anchor = AnchorLayout(size_hint_y=None,height=30)
        self.firstNameInput=CustomTextInput()
        anchor.add_widget(self.firstNameInput)
        firstNameGrid.add_widget(firstNameLabel)
        firstNameGrid.add_widget(anchor)
        grid.add_widget(firstNameGrid)
        
        #Last name
        lastNameGrid = GridLayout(cols=1)
        lastNameLabel = CustomLabel(text="Last name :")
        anchor = AnchorLayout(size_hint_y=None,height=30)
        self.lastNameInput=CustomTextInput()
        anchor.add_widget(self.lastNameInput)
        lastNameGrid.add_widget(lastNameLabel)
        lastNameGrid.add_widget(anchor)
        grid.add_widget(lastNameGrid)
        box.add_widget(grid)
        
        buttonGrid = GridLayout(cols=2,spacing=20,size_hint_y=1)
        confirmButton = CustomButton(text="Confirm")
        cancelButton = CustomButton(text="Cancel")
        confirmButton.bind(on_press=lambda x:write_presence_from_name(values,self.firstNameInput.text,self.lastNameInput.text))
        cancelButton.bind(on_press=lambda x:self.switch_screen(self,"Main"))
        buttonGrid.add_widget(cancelButton)
        buttonGrid.add_widget(confirmButton)
        box.add_widget(buttonGrid)
        
        self.add_widget(box)
        
    def switch_screen(self,instance,screen):
        if screen == "Main":
            Clock.schedule_interval(self.parent.get_screen('Main').update_texture, 1.0 / 60.0)
        self.parent.current = screen