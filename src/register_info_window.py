import kivy
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from custom_button import CustomButton
from custom_label import CustomLabel
import re


class RegisterInfoWindow(Screen):
    def __init__(self,**kwargs):
        super(RegisterInfoWindow, self).__init__(**kwargs)
        self.name = "RegisterInfo"
        self.popup = Popup(title='Oops !',content=Label(text='Hello world'),auto_dismiss=False,size_hint=(.8, .8))
        self.popupIsOpen = False
        main_grid = BoxLayout(orientation="vertical",padding=[20,0,20,0])
        grid = GridLayout(cols=2,padding=[0,100,0,0],spacing=20,size_hint_y=10,col_force_default=True,col_default_width='500')      
        
        #First name
        firstNameGrid = GridLayout(cols=1)
        firstNameLabel = CustomLabel(text="First name :")
        anchor = AnchorLayout(size_hint_y=None,height=30)
        self.firstNameInput=TextInput(multiline=False,size_hint_x=0.5)
        anchor.add_widget(self.firstNameInput)
        firstNameGrid.add_widget(firstNameLabel)
        firstNameGrid.add_widget(anchor)
        grid.add_widget(firstNameGrid)
        
        #Last name
        lastNameGrid = GridLayout(cols=1)
        lastNameLabel = CustomLabel(text="Last name :")
        anchor = AnchorLayout(size_hint_y=None,height=30)
        self.lastNameInput=TextInput(multiline=False,size_hint_x=0.5)
        anchor.add_widget(self.lastNameInput)
        lastNameGrid.add_widget(lastNameLabel)
        lastNameGrid.add_widget(anchor)
        grid.add_widget(lastNameGrid)
        
        #Date of birth
        dobGrid = GridLayout(cols=1)
        dobLabel = CustomLabel(text="Date of birth :")
        anchor = AnchorLayout(size_hint_y=None,height=30)
        self.dobInput=TextInput(multiline=False,size_hint_x=0.5)
        anchor.add_widget(self.dobInput)
        dobGrid.add_widget(dobLabel)
        dobGrid.add_widget(anchor)
        grid.add_widget(dobGrid)
        
        #Telephone
        telephoneGrid = GridLayout(cols=1)
        telephoneLabel = CustomLabel(text="Telephone :")
        anchor = AnchorLayout(size_hint_y=None,height=30)
        self.telephoneInput=TextInput(multiline=False,size_hint_x=0.5)
        anchor.add_widget(self.telephoneInput)
        telephoneGrid.add_widget(telephoneLabel)
        telephoneGrid.add_widget(anchor)
        grid.add_widget(telephoneGrid)  
        
        #Email
        emailGrid = GridLayout(cols=1)
        emailLabel = CustomLabel(text="Email :")
        anchor = AnchorLayout(size_hint_y=None,height=30)
        self.emailInput=TextInput(multiline=False,size_hint_x=0.5)
        anchor.add_widget(self.emailInput)
        emailGrid.add_widget(emailLabel)
        emailGrid.add_widget(anchor)
        grid.add_widget(emailGrid)
        
        #Belt
        beltGrid = GridLayout(cols=1)
        beltLabel = CustomLabel(text="Belt :")
        self.beltDropdown = DropDown()
        ranks = ["white","blue","purple","brown","black"]
        for i in range(len(ranks)):
            btn = Button(text=ranks[i], size_hint_y=None, height=44,on_release=lambda btn: self.beltDropdown.select(btn.text))
            self.beltDropdown.add_widget(btn)
            
        anchor = AnchorLayout(size_hint_y=None,height=30)
        self.beltButton = Button(text="Belt rank",size_hint_x=0.5,size_hint_y=None,height='48dp')
        self.beltButton.bind(on_release=self.beltDropdown.open)
        self.beltDropdown.bind(on_select=lambda instance, x: setattr(self.beltButton, 'text', x))
        beltGrid.add_widget(beltLabel)
        beltGrid.add_widget(self.beltButton)
        grid.add_widget(beltGrid)
        
        button_grid = GridLayout(cols=2,spacing=20,size_hint_y=1)
        confirmButton = CustomButton(text="Confirm")
        cancelButton = CustomButton(text="Cancel")
        confirmButton.bind(on_press=self.confirm)
        cancelButton.bind(on_press=lambda x:self.switch_screen(self,"Main"))
        button_grid.add_widget(cancelButton)
        button_grid.add_widget(confirmButton)
        
        main_grid.add_widget(grid)
        main_grid.add_widget(button_grid)
        
        self.add_widget(main_grid)
        
    def validate(self):
        inputs = [self.firstNameInput,self.lastNameInput,self.dobInput,self.telephoneInput,self.emailInput]
        valid = True
        if not re.search("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$",self.firstNameInput.text):
            message = "Please enter a valid first name"
            valid = False
        if not re.search("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$",self.lastNameInput.text):
            message = "Please enter a valid last name"
            valid = False
        if not re.search("^(0?[1-9]|[12][0-9]|3[01])\/(0?[1-9]|1[012])\/\d{4}$",self.dobInput.text):
            message = "Please enter a valid date of birth"
            valid = False
        if not re.search("^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$",self.telephoneInput.text):
            message = "Please enter a valid telephone number"
            valid = False
        if not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',self.emailInput.text):
            message = "Please enter a valid email"
            valid = False
        for i in inputs:
            if i.text == "":
                valid = False
        if not valid:
            print("Invalid")
            self.popup.content = Label(text=message)
            self.popupIsOpen = True
            self.popup.open()
            Clock.schedule_once(self.close_popup, 2)
            return False
        return True
    
    def close_popup(self,instance):
        """
            Closes the popup
        """
        self.popup.dismiss()
        self.popupIsOpen = False
        
    def confirm(self,instance):
        if self.validate():
            self.switch_screen(self,"RegisterPhoto")
        
    def switch_screen(self,instance,screen):
        if screen == "Main":
            Clock.schedule_interval(self.parent.get_screen('Main').update_texture, 1.0 / 60.0)
        self.parent.current = screen