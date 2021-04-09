"""
    Handles the face recognition and face detection.
"""

import cv2
import face_recognition
import numpy as np
import info

# Array of recognized faces so far, so that a user is not marked as present more than once.
recognized_faces = []


def get_faces(frame):
    """
        Detects faces on an image

        :param frame: image on which we wish to detect faces

        :return: encodings of detected faces, and locations of detected faces
    """
    # Resize and transform the image to RGB
    resized_image = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

    # Detect the faces
    webcam_faces = face_recognition.face_locations(resized_image)
    webcam_encoding = face_recognition.face_encodings(
        resized_image, webcam_faces)
    return webcam_encoding, webcam_faces


def get_matches(frame, known_encodings, users):
    """
        Finds out the identities of the people recognized on an image.

        :param frame: image on which we wish to identify users
        :param known_encodings: face encodings of all registered users
        :param users: list of registered users

        :return frame: updated image with squares around recognized/detected
                       faces
        :return recognized_users: list of users recognized on the given image
    """
    # Get detected faces (encodings and positions)
    webcam_encoding, webcam_faces = get_faces(frame)

    # Array of all recognized users on the given image
    recognized_users = []

    # Go throuh all detected faces on the image
    for encoded_face, face_location in zip(webcam_encoding, webcam_faces):
        # Find matches
        matches = face_recognition.compare_faces(known_encodings, encoded_face)

        # Compute face distances (aka how similar 2 face encodings are)
        face_distances = face_recognition.face_distance(
            known_encodings, encoded_face)

        # There is a match
        if len(face_distances) > 0:
            match_id = np.argmin(face_distances)

            if matches[match_id]:
                # Append the id of the user to the recognized users
                if info.users[match_id]["_id"] not in recognized_faces:
                    recognized_users.append(info.users[match_id])
                    recognized_faces.append(info.users[match_id]["_id"])

                # Draw a square around the recognized faces, with a text
                # containing their names
                y1, x2, y2, x1 = face_location
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255, 255), 4)
                cv2.rectangle(frame, (x1, y2-35), (x2, y2),
                              (0, 0, 255, 255), cv2.FILLED)
                cv2.putText(img=frame, text=users[match_id]["name"], org=(
                    x1+6, y2-6), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=[255, 255, 255, 255], lineType=cv2.LINE_AA, thickness=2)

            # A face was detected but not recognizes, a square is drawn but no
            # name is displayed
            else:
                y1, x2, y2, x1 = face_location
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255, 255), 4)
                cv2.rectangle(frame, (x1, y2-35), (x2, y2),
                              (0, 0, 255, 255), cv2.FILLED)
                cv2.putText(img=frame, text=users[match_id]["?"], org=(
                    x1+6, y2-6), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=[255, 255, 255, 255], lineType=cv2.LINE_AA, thickness=2)
    return frame, recognized_users


def get_faces_frame(frame):
    """
        Returns a frame with squares around all faces

        :param frame: given image

        :return frame: modified image
        :return webcam_encoding: encodings of faces on the image
    """
    webcam_encoding, webcam_faces = get_faces(frame)
    if len(webcam_faces) > 0:
        y1, x2, y2, x1 = webcam_faces[0]
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255, 255), 4)
    return frame, webcam_encoding
