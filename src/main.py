"""
    Main file, lauches the kivy application.
"""
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')
from Windows.problem_window import ProblemWindow
from Windows.already_member_photo_window import AlreadyMemberPhotoWindow
from Windows.already_member_window import AlreadyMemberWindow
from Windows.register_photo_window import RegisterPhotoWindow
from Windows.register_info_window import RegisterInfoWindow
from Windows.main_window import MainWindow
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.camera import Camera
from kivy.uix.vkeyboard import VKeyboard
from kivy.core.window import Window
from kivy.app import App
import info
import kivy


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
