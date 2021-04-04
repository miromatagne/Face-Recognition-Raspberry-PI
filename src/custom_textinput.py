import kivy
from kivy.uix.textinput import TextInput
from kivy.lang import Builder

Builder.load_file('custom_textinput.kv')

class CustomTextInput(TextInput):
    pass
