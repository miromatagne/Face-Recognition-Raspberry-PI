"""
    Already Member Photo Window : takes a picture of a user that is
    registered in the spreadsheet but not in the database, and stores 
    the encoded face in the database.
    Contains : 
        -an image representing the live feed from the camera
        -a text indicating the user what to do
        -a countdown text
        -2 buttons to confirm or cancel
"""

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
import cv2
import face_recognition
import numpy as np
from faces import get_matches, get_faces_frame
from participant_list import add_user, write_new_id, get_sheet_content, write_presence, write_presence_from_name
from database import post_to_db, get_documents
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from custom_button import CustomButton
import time
import info


class AlreadyMemberPhotoWindow(Screen):
    def __init__(self, cam, **kwargs):
        super(AlreadyMemberPhotoWindow, self).__init__(**kwargs)
        self.name = "AlreadyMemberPhoto"
        grid = GridLayout(cols=1)

        # Image displaying the live feed from the camera
        self.img = Image(size_hint_y=10)
        grid.add_widget(self.img)

        # Text indicating the user what to do
        self.info_label = Label(
            text="Press the confirm button, a picture of you will be taken in 5 seconds. Make sure your face is clearly visible !")
        grid.add_widget(self.info_label)
        subgrid = GridLayout(cols=3, size_hint_y=1)

        # Buttons
        cancel_button = CustomButton(text="Cancel")
        cancel_button.bind(
            on_press=lambda x: self.switch_screen(self, "AlreadyMember"))
        photo_button = CustomButton(text="Go")
        photo_button.bind(on_press=self.start_capture)

        # Countdown text
        self.countdown_text = Label(text="5")

        subgrid.add_widget(self.countdown_text)
        subgrid.add_widget(cancel_button)
        subgrid.add_widget(photo_button)
        grid.add_widget(subgrid)
        self.add_widget(grid)
        self.cam = cam

        # Update the image every 10ms
        Clock.schedule_interval(self.update_texture, 1.0 / 100.0)

    def update_texture(self, instance):
        """
            Updates the live camera stream and calls the face detection
            functions. Draws squares around detected faces.
        """
        # Get image frame from camera and reshape it
        frame = np.frombuffer(self.cam.texture.pixels, np.uint8)
        frame = frame.reshape(
            (self.cam.texture.size[1], self.cam.texture.size[0], 4))

        # Get detected faces from the actual frame
        frame, encodings = get_faces_frame(frame)

        # If the countdown is done, notify the user and register him
        if(self.countdown_text.text.isnumeric() and int(self.countdown_text.text) == 0):
            self.countdown_text.text = "Done !"

            # A face was detected
            if(len(encodings) > 0):
                self.info_label.text = "Your registration was successful, you will be redirected towards the main screen."
                user = self.parent.get_screen("AlreadyMember").selectedMember

                # Update the database
                user_id = post_to_db(
                    user[0], user[1], user[6], user[4], user[5], user[9], encodings[0].tolist())

                # Update the spreadsheet (should contain the new Id of the user)
                write_new_id(info.values, self.parent.get_screen(
                    "AlreadyMember").selected_member_index, user_id)
                Clock.schedule_once(
                    lambda x: self.switch_screen(self, "Main"), 2.0)

            # No face was detected
            else:
                self.countdown_text.text = "5"
                self.info_label.text = "Your face was not recognized, please try again"

        # Adjust image frame and display it
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

    def decrement_countdown(self, instance):
        """
            Decrements the countdown by 1
        """
        self.countdown_text.text = str(int(self.countdown_text.text) - 1)

    def start_capture(self, instance):
        """
            Starts the image capture : every second it calls the decrement_countdown
            function until it reaches 0.
        """
        Clock.schedule_once(self.decrement_countdown, 1)
        Clock.schedule_once(self.decrement_countdown, 2)
        Clock.schedule_once(self.decrement_countdown, 3)
        Clock.schedule_once(self.decrement_countdown, 4)
        Clock.schedule_once(self.decrement_countdown, 5)

    def switch_screen(self, instance, screen):
        """
            Switches to another screen of the kivy app

            :param screen: name of the screen the app should switch to
        """
        if screen == "Main":
            Clock.schedule_interval(self.parent.get_screen(
                'Main').update_texture, 1.0 / 60.0)
        self.parent.current = screen
