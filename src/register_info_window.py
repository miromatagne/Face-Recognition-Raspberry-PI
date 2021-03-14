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
        grid = GridLayout(cols=2,padding=30,size_hint_x=None,col_force_default=True,col_default_width='500')      
        
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
        lastNameLabel = Label(text="Last name :",size_hint_y=None,height=30)
        anchor = AnchorLayout(size_hint_y=None,height=30)
        self.lastNameInput=TextInput(multiline=False,size_hint_x=0.5)
        anchor.add_widget(self.lastNameInput)
        lastNameGrid.add_widget(lastNameLabel)
        lastNameGrid.add_widget(anchor)
        grid.add_widget(lastNameGrid)
        
        #Date of birth
        dobGrid = GridLayout(cols=1)
        dobLabel = Label(text="Date of birth :",size_hint_y=None,height=30)
        anchor = AnchorLayout(size_hint_y=None,height=30)
        self.dobInput=TextInput(multiline=False,size_hint_x=0.5)
        anchor.add_widget(self.dobInput)
        dobGrid.add_widget(dobLabel)
        dobGrid.add_widget(anchor)
        grid.add_widget(dobGrid)
        
        #Telephone
        telephoneGrid = GridLayout(cols=1)
        telephoneLabel = Label(text="Telephone :",size_hint_y=None,height=30)
        anchor = AnchorLayout(size_hint_y=None,height=30)
        self.telephoneInput=TextInput(multiline=False,size_hint_x=0.5)
        anchor.add_widget(self.telephoneInput)
        telephoneGrid.add_widget(telephoneLabel)
        telephoneGrid.add_widget(anchor)
        grid.add_widget(telephoneGrid)  
        
        #Email
        emailGrid = GridLayout(cols=1)
        emailLabel = Label(text="Email :",size_hint_y=None,height=30)
        anchor = AnchorLayout(size_hint_y=None,height=30)
        self.emailInput=TextInput(multiline=False,size_hint_x=0.5)
        anchor.add_widget(self.emailInput)
        emailGrid.add_widget(emailLabel)
        emailGrid.add_widget(anchor)
        grid.add_widget(emailGrid)
        
        #Belt
        beltGrid = GridLayout(cols=1)
        beltLabel = Label(text="Belt :",size_hint_y=None,height=30)
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
        
        confirmButton = Button(text="Confirm",size_hint_y=None,height='48dp')
        cancelButton = Button(text="Cancel",size_hint_y=None,height='48dp')
        confirmButton.bind(on_press=self.confirm)
        cancelButton.bind(on_press=lambda x:self.switch_screen(self,"Main"))
        grid.add_widget(confirmButton)
        grid.add_widget(cancelButton)
        
        self.add_widget(grid)
        
    def validate(self):
        inputs = [self.firstNameInput,self.lastNameInput,self.dobInput,self.telephoneInput,self.emailInput]
        for i in inputs:
            if i.text == "":
                return False
        return True
        
    def confirm(self,instance):
        if self.validate():
            self.switch_screen(self,"RegisterPhoto")
        
    def switch_screen(self,instance,screen):
        if screen == "Main":
            Clock.schedule_interval(self.parent.get_screen('Main').update_texture, 1.0 / 60.0)
        self.parent.current = screen