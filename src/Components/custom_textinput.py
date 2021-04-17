"""
    Custom TextInput Component.
    Loads the text input UI from the corresponding kv file.
"""

import kivy
from kivy.uix.textinput import TextInput
from kivy.lang import Builder

Builder.load_file('Components/custom_textinput.kv')


class CustomTextInput(TextInput):
    pass
