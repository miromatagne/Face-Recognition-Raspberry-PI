import kivy
from kivy.uix.button import Button
from kivy.lang import Builder

Builder.load_file('custom_button.kv')

class CustomButton(Button):
    pass