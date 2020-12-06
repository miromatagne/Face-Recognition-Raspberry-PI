import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder


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
