"""
    Register Info Window. 
    Contains : 
        -text inputs asking for the user's first name, last name,
        date of birth, telephone, email, and belt rank
        -2 buttons allowing to confirm or cancel
"""

import kivy
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.clock import Clock
from custom_button import CustomButton
from custom_label import CustomLabel
from custom_textinput import CustomTextInput
from custom_popup import CustomPopup
import re


class RegisterInfoWindow(Screen):
    def __init__(self, **kwargs):
        super(RegisterInfoWindow, self).__init__(**kwargs)
        self.name = "RegisterInfo"

        # Popup when there is an error
        self.popup = CustomPopup(
            title='Oops !', content=Label(text='Hello world'))
        self.popup_is_open = False

        main_layout = BoxLayout(orientation="vertical", padding=[20, 0, 20, 0])
        grid = GridLayout(cols=2, padding=[
                          0, 100, 0, 0], spacing=20, size_hint_y=10, col_force_default=True, col_default_width='400')

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
        last_name_label = CustomLabel(text="Last name :")
        anchor = AnchorLayout(size_hint_y=None, height=30)
        self.last_name_input = CustomTextInput()
        anchor.add_widget(self.last_name_input)
        last_name_grid.add_widget(last_name_label)
        last_name_grid.add_widget(anchor)
        grid.add_widget(last_name_grid)

        # Date of birth
        dob_grid = GridLayout(cols=1)
        dob_label = CustomLabel(text="Date of birth :")
        anchor = AnchorLayout(size_hint_y=None, height=30)
        self.dob_input = CustomTextInput()
        anchor.add_widget(self.dob_input)
        dob_grid.add_widget(dob_label)
        dob_grid.add_widget(anchor)
        grid.add_widget(dob_grid)

        # Telephone
        telephone_grid = GridLayout(cols=1)
        telephone_label = CustomLabel(text="Telephone :")
        anchor = AnchorLayout(size_hint_y=None, height=30)
        self.telephone_input = CustomTextInput()
        anchor.add_widget(self.telephone_input)
        telephone_grid.add_widget(telephone_label)
        telephone_grid.add_widget(anchor)
        grid.add_widget(telephone_grid)

        # Email
        email_grid = GridLayout(cols=1)
        email_label = CustomLabel(text="Email :")
        anchor = AnchorLayout(size_hint_y=None, height=30)
        self.email_input = CustomTextInput()
        anchor.add_widget(self.email_input)
        email_grid.add_widget(email_label)
        email_grid.add_widget(anchor)
        grid.add_widget(email_grid)

        # Belt
        belt_grid = GridLayout(cols=1)
        belt_label = CustomLabel(text="Belt :")
        self.belt_dropdown = DropDown()
        self.belt_dropdown.container.spacing = 10
        self.belt_dropdown.container.padding = [0, 0, 0, 10]
        with self.belt_dropdown.container.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(
                size=self.belt_dropdown.container.size, pos=self.belt_dropdown.container.pos)

        # Add all belt ranks to dropdown
        ranks = ["white", "blue", "purple", "brown", "black"]
        for i in range(len(ranks)):
            btn = CustomButton(
                text=ranks[i], height=30, on_release=lambda btn: self.belt_dropdown.select(btn.text))
            self.belt_dropdown.add_widget(btn)

        anchor = AnchorLayout(size_hint_x=1, size_hint_y=None,
                              height=30, padding=[20, 0, 20, 0])
        self.belt_button = CustomButton(
            text="Select belt rank", size_hint_x=0.5, height=30)
        self.belt_button.bind(on_release=self.belt_dropdown.open)
        self.belt_dropdown.bind(on_select=lambda instance,
                                x: setattr(self.belt_button, 'text', x))
        anchor.add_widget(self.belt_button)
        belt_grid.add_widget(belt_label)
        belt_grid.add_widget(anchor)
        grid.add_widget(belt_grid)

        button_grid = GridLayout(cols=2, spacing=20, size_hint_y=1)
        confirm_button = CustomButton(text="Confirm")
        cancel_button = CustomButton(text="Cancel")
        confirm_button.bind(on_press=self.confirm)
        cancel_button.bind(on_press=lambda x: self.switch_screen(self, "Main"))
        button_grid.add_widget(cancel_button)
        button_grid.add_widget(confirm_button)

        main_layout.add_widget(grid)
        main_layout.add_widget(button_grid)

        self.add_widget(main_layout)

    def validate(self):
        """
            Check if all inputs are valid and respect the corresponding regular expressions.

            :return: True if valid, False otherwise
        """
        inputs = [self.first_name_input, self.last_name_input,
                  self.dob_input, self.telephone_input, self.email_input]
        valid = True
        if not re.search("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$", self.first_name_input.text):
            message = "Please enter a valid first name"
            valid = False
        if not re.search("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$", self.last_name_input.text):
            message = "Please enter a valid last name"
            valid = False
        if not re.search("^(0?[1-9]|[12][0-9]|3[01])\/(0?[1-9]|1[012])\/\d{4}$", self.dob_input.text):
            message = "Please enter a valid date of birth"
            valid = False
        if not re.search("^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$", self.telephone_input.text):
            message = "Please enter a valid telephone number"
            valid = False
        if not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', self.email_input.text):
            message = "Please enter a valid email"
            valid = False
        for i in inputs:
            if i.text == "":
                valid = False
        if not valid:
            self.popup.content = Label(text=message)
            self.popup_is_open = True
            self.popup.open()
            Clock.schedule_once(self.close_popup, 2)
            return False
        return True

    def close_popup(self, instance):
        """
            Closes the popup
        """
        self.popup.dismiss()
        self.popup_is_open = False

    def confirm(self, instance):
        """
            Executed when the user confirms his inputs.
            After validation, the app navigates to another screen.
        """
        if self.validate():
            self.switch_screen(self, "RegisterPhoto")

    def switch_screen(self, instance, screen):
        """
            Switches to another screen of the kivy app

            :param screen: name of the screen the app should switch to
        """
        if screen == "Main":
            Clock.schedule_interval(self.parent.get_screen(
                'Main').update_texture, 1.0 / 60.0)
        self.parent.current = screen
