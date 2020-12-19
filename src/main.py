import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.camera import Camera
from kivy.lang import Builder
import cv2
import numpy as np
import faces
    

class MainWindow(Screen):
    pass


class SecondWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("ui.kv")


class Program(App):
    def build(self):
        return kv


if __name__ == "__main__":
    Program().run()
