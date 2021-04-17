"""
    Main Window. 
    Contains : 
        -live image from the camera, where recognized users are represented with
        a square around their face, and a sound is produced when recognized
        -3 buttons allowing to navigate to other screens of the app
"""

import info
from Components.custom_popup import CustomPopup
from Components.custom_button import CustomButton
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from participant_list import write_presence
from faces import get_matches
import numpy as np
import cv2
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import kivy
import os
os.environ['KIVY_AUDIO'] = 'sdl2'


class MainWindow(Screen):
    def __init__(self, cam, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.name = "Main"
        grid = GridLayout(cols=1, spacing=20, padding=[20, 0, 20, 20])

        # Image containing live feed from the camera
        self.img = Image(size_hint_y=10)
        grid.add_widget(self.img)

        # Buttons
        subgrid = GridLayout(cols=3, size_hint_y=1, spacing=20)
        register_button = CustomButton(text="Register")
        already_member_button = CustomButton(text="Already a member ?")
        problem_button = CustomButton(text="Problem ?")
        register_button.bind(
            on_press=lambda x: self.switch_screen(self, "RegisterInfo"))
        already_member_button.bind(
            on_press=lambda x: self.switch_screen(self, "AlreadyMember"))
        problem_button.bind(
            on_press=lambda x: self.switch_screen(self, "Problem"))
        subgrid.add_widget(register_button)
        subgrid.add_widget(already_member_button)
        subgrid.add_widget(problem_button)
        grid.add_widget(subgrid)
        self.add_widget(grid)

        # Popup when user is recognized
        self.popup = CustomPopup(
            title='Welcome !', content=Label(text='Hello world'))
        self.popup_is_open = False
        self.cam = cam

        # Update the image every 10ms.
        Clock.schedule_interval(self.update_texture, 1.0 / 100.0)

    def update_texture(self, instance):
        """
            Updates the live camera stream and calls the face recognition
            functions. Draws squares around recognized faces, opens
            the popup and plays a sound when a face has been recognized.
        """
        # Get image frame from camera and reshape it
        frame = np.frombuffer(self.cam.texture.pixels, np.uint8)
        frame = frame.reshape(
            (self.cam.texture.size[1], self.cam.texture.size[0], 4))

        # Get recognized users from the actual frame
        frame, recognized_users = get_matches(
            frame, info.known_encodings, info.users)

        # If a user (or users) was (were) recognized, open popup and play sound
        if len(recognized_users) != 0 and not self.popup_is_open:
            popup_text = "Welcome "
            for n in recognized_users:
                popup_text += n["name"] + ' '
            popup_text += '!'
            self.popup.content = Label(text=popup_text)
            self.popup_is_open = True
            self.popup.open()

            # Play sound
            sound = SoundLoader.load('ding.wav')
            if sound:
                print("Sound found at %s" % sound.source)
                print("Sound is %.3f seconds" % sound.length)
                sound.play()
                sound.seek(0.00)

            # Mark all recognized users as present in the spreadsheet
            for n in recognized_users:
                write_presence(info.values, n["_id"])

            # CLose the popup 2 seconds later
            Clock.schedule_once(self.close_popup, 2)

        # Process frame before displaying it
        window_shape = Window.size
        window_width = window_shape[0]
        window_height = window_shape[1]
        frame = cv2.resize(frame, (int(
            window_height * (self.cam.texture.size[0]/self.cam.texture.size[1])), window_height))
        frame = frame.reshape((frame.shape[1], frame.shape[0], 4))
        buf = frame.tobytes()
        texture = Texture.create(
            size=(frame.shape[0], frame.shape[1]), colorfmt='rgba')
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()
        self.img.texture = texture

    def close_popup(self, instance):
        """
            Closes the popup
        """
        self.popup.dismiss()
        self.popup_is_open = False

    def switch_screen(self, instance, screen):
        """
            Switches to another screen of the kivy app

            :param screen: name of the screen the app should switch to
        """
        Clock.unschedule(self.update_texture)
        self.parent.current = screen
