"""
    Custom Label Component.
    Loads the label UI from the corresponding kv file.
"""

import kivy
from kivy.uix.label import Label
from kivy.lang import Builder

Builder.load_file('custom_label.kv')


class CustomLabel(Label):
    pass
