import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
import time
import info


class AlreadyMemberWindow(Screen):
    def __init__(self,**kwargs):
        super(AlreadyMemberWindow, self).__init__(**kwargs)
        self.name = "AlreadyMember"
        self.grid = GridLayout(cols=1,padding=[0,50,0,50])
        
        self.selectedMember = None
        
        subgrid = GridLayout(cols=2,size_hint_y=10)
        
        inputGrid = GridLayout(cols=1)
        nameLabel = Label(text="Name :",size_hint_y=None,height=30)
        anchor = AnchorLayout(size_hint_y=None,height=30)
        self.nameInput=TextInput(multiline=False,size_hint_x=0.5)
        self.nameInput.bind(text=lambda x,y:self.update_list(self))
        anchor.add_widget(self.nameInput)
        inputGrid.add_widget(nameLabel)
        inputGrid.add_widget(anchor)
        subgrid.add_widget(inputGrid)
        
        self.listScroll = ScrollView(size_hint=(1,1))
        subgrid.add_widget(self.listScroll)
        
        self.grid.add_widget(subgrid)
        
        button_grid = GridLayout(cols=2,size_hint_y=1)
        confirmButton = Button(text="Confirm",size_hint_y=None,height='48dp')
        cancelButton = Button(text="Cancel",size_hint_y=None,height='48dp')
        confirmButton.bind(on_press=lambda x:self.update_list(self))
        cancelButton.bind(on_press=lambda x:self.switch_screen(self,"Main"))
        
        button_grid.add_widget(cancelButton)
        button_grid.add_widget(confirmButton)
        
        self.grid.add_widget(button_grid)
        
        self.add_widget(self.grid)
    
    def update_list(self,instance):
        self.listScroll.clear_widgets()
        listGrid = GridLayout(cols=1,spacing=10,size_hint_y=None)
        listGrid.bind(minimum_height=listGrid.setter('height'))
        #print(info.values)
        for i in range(len(info.values)):
            name = info.values[i][0] + " " + info.values[i][1]
            #print(name)
            if len(self.nameInput.text) > 2 and (self.nameInput.text).lower() in name.lower():
                btn = Button(text=name,size_hint_y=None,height='48dp')
                btn.bind(on_press=lambda *args, i=i: self.select_member(self,i))
                listGrid.add_widget(btn)
        self.listScroll.add_widget(listGrid)
        
    def switch_screen(self,instance,screen):
        if screen == "Main":
            Clock.schedule_interval(self.parent.get_screen('Main').update_texture, 1.0 / 60.0)
        self.parent.current = screen
        
    def select_member(self,instance,i):
        self.selectedMember = info.values[i]
        self.switch_screen(self,"AlreadyMemberPhoto")
        
