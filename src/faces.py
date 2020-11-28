import cv2
import face_recognition
import numpy as np


def get_face_encodings(images):
    # Returns the encodings from an array of images
    encodings = []
    for im in images:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(im)[0]
        encodings.append(encode)
    return encodings


# Captures video from camera, should be replaced with
# a function to capture the Raspberry Pi camera.
cap = cv2.VideoCapture(0)


def get_matches(im, known_encodings):
    # Returns the identities of the people recognized on an image
    success, im = cap.read()
    resizedImage = cv2.resize(im, (0, 0), None, 0.25, 0.25)
    resizedImage = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2RGB)

    webcamFaces = face_recognition.face_locations(resizedImage)
    webcamEncoding = face_recognition.face_encodings(resizedImage, webcamFaces)

    for encodedFace, faceLocation in zip(webcamEncoding, webcamFaces):
        matches = face_recognition.compare_faces(known_encodings, encodedFace)
        faceDistances = face_recognition.face_distance(
            known_encodings, encodedFace)

        match_id = np.argmin(faceDistances)
        if matches[match_id]:
            # TODO replace following with something we can use to
            # find id (dictionnary, ...)
            name = fileList[matchId]
            print(name)
            y1, x2, y2, x1 = faceLocation
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(im, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.rectangle(im, (x1, y2-35), (x2, y2), (255, 0, 0), cv2.FILLED)
            cv2.putText(im, name.split(".")[0], (x1+6, y2-6),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
