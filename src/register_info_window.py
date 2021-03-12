import kivy
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.anchorlayout import AnchorLayout


class RegisterInfoWindow(Screen):
    def __init__(self,**kwargs):
        super(RegisterInfoWindow, self).__init__(**kwargs)
        self.name = "RegisterInfo"
        grid = GridLayout(cols=2,size_hint_x=None,col_force_default=True,col_default_width='500')      
        
        #First name
        firstNameGrid = GridLayout(cols=1)
        firstNameLabel = Label(text="First name :",size_hint_y=None,height=30)
        anchor = AnchorLayout(size_hint_y=None,height=30)
        self.firstNameInput=TextInput(multiline=False,size_hint_x=0.5)
        anchor.add_widget(self.firstNameInput)
        firstNameGrid.add_widget(firstNameLabel)
        firstNameGrid.add_widget(anchor)
        grid.add_widget(firstNameGrid)
        
        #Last name
        lastNameGrid = GridLayout(cols=1)
        lastNameLabel = Label(text="Last name :")
        self.lastNameInput=TextInput(multiline=False)
        lastNameGrid.add_widget(lastNameLabel)
        lastNameGrid.add_widget(self.lastNameInput)
        grid.add_widget(lastNameGrid)
        
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
        cancelButton.bind(on_press=lambda x:self.switch_screen(self,"Main"))
        grid.add_widget(confirmButton)
        grid.add_widget(cancelButton)
        
        self.add_widget(grid)
        
    def switch_screen(self,instance,screen):
        if screen == "Main":
            Clock.schedule_interval(self.parent.get_screen('Main').update_texture, 1.0 / 60.0)
        self.parent.current = screen