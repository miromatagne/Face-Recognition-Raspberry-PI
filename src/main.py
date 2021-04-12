"""
    Main file, lauches the kivy application.
"""

from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')
import kivy
import info
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.camera import Camera
from kivy.uix.screenmanager import ScreenManager

from main_window import MainWindow
from register_info_window import RegisterInfoWindow
from register_photo_window import RegisterPhotoWindow
from already_member_window import AlreadyMemberWindow
from already_member_photo_window import AlreadyMemberPhotoWindow
from problem_window import ProblemWindow
          
class Program(App):
    def build(self):
        self.cam = Camera(play=True)
        sm = ScreenManager()
        sm.add_widget(MainWindow(self.cam))
        sm.add_widget(RegisterInfoWindow())
        sm.add_widget(RegisterPhotoWindow(self.cam))
        sm.add_widget(ProblemWindow())
        sm.add_widget(AlreadyMemberWindow())
        sm.add_widget(AlreadyMemberPhotoWindow(self.cam))
        return sm

if __name__ == "__main__":
    """
        Sets the app to fullscreen mode and calls the info file to 
        retreive important information .
    """
    Window.fullscreen = 'auto'
    Window.clearcolor = (1, 1, 1, 1)
    info.init()
    Program().run()
