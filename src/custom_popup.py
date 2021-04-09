"""
    Custom Popup Component.
    Loads the popup UI from the corresponding kv file.
"""

import kivy
from kivy.uix.popup import Popup
from kivy.lang import Builder

Builder.load_file('custom_popup.kv')


class CustomPopup(Popup):
    pass
