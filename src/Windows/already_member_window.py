"""
    Already Member Window : allows user who are already registered in the
    spreadsheet to register to the database too (have their faces encoded).
    Contains : 
        -a text input where the user can search for his name
        -a scrolldown menu where the user can pick his name
"""

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
from Components.custom_button import CustomButton
from Components.custom_textinput import CustomTextInput
from Components.custom_label import CustomLabel
from Components.custom_popup import CustomPopup
import time
import info


class AlreadyMemberWindow(Screen):
    def __init__(self, **kwargs):
        super(AlreadyMemberWindow, self).__init__(**kwargs)
        self.name = "AlreadyMember"
        self.grid = GridLayout(cols=1, padding=[20, 100, 20, 30])

        # Initialize the selected user/member to None
        self.selected_member = None

        subgrid = GridLayout(cols=2, size_hint_y=10)

        input_grid = GridLayout(cols=1)

        # Name input
        name_label = CustomLabel(text="Name :")
        anchor = AnchorLayout(size_hint_y=None, height=30)
        self.name_input = CustomTextInput()
        self.name_input.bind(text=lambda x, y: self.update_list(self))
        anchor.add_widget(self.name_input)
        input_grid.add_widget(name_label)
        input_grid.add_widget(anchor)
        subgrid.add_widget(input_grid)

        # Scrolldown menu
        self.list_scroll = ScrollView(size_hint=(1, 1))
        subgrid.add_widget(self.list_scroll)

        self.grid.add_widget(subgrid)

        # Buttons
        button_grid = GridLayout(cols=2, size_hint_y=1, spacing=20)
        confirm_button = CustomButton(text="Confirm")
        cancel_button = CustomButton(text="Cancel")
        confirm_button.bind(on_press=lambda x: self.update_list(self))
        cancel_button.bind(on_press=lambda x: self.switch_screen(self, "Main"))

        button_grid.add_widget(cancel_button)
        button_grid.add_widget(confirm_button)

        self.grid.add_widget(button_grid)

        self.add_widget(self.grid)

        # Popup
        self.popup = CustomPopup(
            title='Welcome !', content=Label(text='Hello world'))

    def update_list(self, instance):
        """
            Every time the user modifies the input in the text input,
            the scrolldown list is updated with the appropriate names.
        """
        self.list_scroll.clear_widgets()
        list_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        list_grid.bind(minimum_height=list_grid.setter('height'))

        # Go through all names in the spreadsheet
        for i in range(len(info.values)):
            name = info.values[i][0] + " " + info.values[i][1]

            # Check if the input text is contained in a name in the spreadsheet
            if len(self.name_input.text) > 2 and (self.name_input.text).lower() in name.lower():
                btn = CustomButton(text=name, size_hint_y=None, height='48dp')
                btn.bind(on_press=lambda *args,
                         i=i: self.select_member(self, i))
                list_grid.add_widget(btn)
        self.list_scroll.add_widget(list_grid)

    def switch_screen(self, instance, screen):
        """
            Switches to another screen of the kivy app

            :param screen: name of the screen the app should switch to
        """
        if screen == "Main":
            Clock.schedule_interval(self.parent.get_screen(
                'Main').update_texture, 1.0 / 100.0)
        self.parent.current = screen

    def select_member(self, instance, i):
        """
            Executes when the user selects a name in the scrolldown list.
            Verifies if the selected name is not already registered in the 
            database, and if it is the case, shows an error popup. Else,
            navigates to the next screen.

            :param i: index of the selected member
        """
        user_exists = False
        # Check if user already exists in the database
        for db_user in info.users:
            if len(info.values[i]) > 2: 
                if db_user["_id"] == info.values[i][2]:
                    user_exists = True
                    break

        # If user does not exists, navigate to next screen
        if not user_exists:
            self.selected_member = info.values[i]
            self.selected_member_index = i
            self.switch_screen(self, "AlreadyMemberPhoto")

        # Else, show an error popup
        else:
            self.popup.content = Label(
                text="Your face is already registered, you will be redirected to the main page.")
            self.popup.open()
            Clock.schedule_once(self.user_already_registered, 3)

    def user_already_registered(self, instance):
        """
            Closes the popup and navigates back to the main screen if
            the selected user already exists
        """
        self.popup.dismiss()
        self.switch_screen(self, 'Main')
