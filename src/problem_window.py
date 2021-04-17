"""
    Problem Window. 
    Contains : 
        -2 text inputs where the user can register with his first name 
        and last name in case the face recognition dod not work
        -2 buttons to confirm or cancel
"""

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
from Components.custom_button import CustomButton
from Components.custom_label import CustomLabel
from Components.custom_textinput import CustomTextInput


class ProblemWindow(Screen):
    def __init__(self, **kwargs):
        super(ProblemWindow, self).__init__(**kwargs)
        self.name = "Problem"

        box = BoxLayout(spacing=20, orientation="vertical",
                        padding=[20, 20, 20, 20])
        grid = GridLayout(cols=2, padding=[0, 100, 0, 0], size_hint_y=10)

        # First name
        first_name_grid = GridLayout(cols=1)
        first_name_label = CustomLabel(text="First name :")
        anchor = AnchorLayout(size_hint_y=None, height=30)
        self.first_name_input = CustomTextInput()
        anchor.add_widget(self.first_name_input)
        first_name_grid.add_widget(first_name_label)
        first_name_grid.add_widget(anchor)
        grid.add_widget(first_name_grid)

        # Last name
        last_name_grid = GridLayout(cols=1)
        lastNameLabel = CustomLabel(text="Last name :")
        anchor = AnchorLayout(size_hint_y=None, height=30)
        self.lastNameInput = CustomTextInput()
        anchor.add_widget(self.lastNameInput)
        last_name_grid.add_widget(lastNameLabel)
        last_name_grid.add_widget(anchor)
        grid.add_widget(last_name_grid)
        box.add_widget(grid)

        # Buttons
        button_grid = GridLayout(cols=2, spacing=20, size_hint_y=1)
        confirm_button = CustomButton(text="Confirm")
        cancel_button = CustomButton(text="Cancel")
        confirm_button.bind(on_press=lambda x: write_presence_from_name(
            info.values, self.first_name_input.text, self.lastNameInput.text))
        cancel_button.bind(on_press=lambda x: self.switch_screen(self, "Main"))
        button_grid.add_widget(cancel_button)
        button_grid.add_widget(confirm_button)
        box.add_widget(button_grid)

        self.add_widget(box)

    def switch_screen(self, instance, screen):
        """
            Switches to another screen of the kivy app

            :param screen: name of the screen the app should switch to
        """
        if screen == "Main":
            Clock.schedule_interval(self.parent.get_screen(
                'Main').update_texture, 1.0 / 60.0)
        self.parent.current = screen
