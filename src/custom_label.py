import kivy
from kivy.uix.label import Label
from kivy.lang import Builder

Builder.load_file('custom_label.kv')

class CustomLabel(Label):
    pass