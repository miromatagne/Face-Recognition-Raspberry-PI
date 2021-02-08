import cv2
import face_recognition
import numpy as np

recognizedFaces = []

def find_encodings(images):
    """
        Returns the encoded versions of an array of images
    """
    encodings = []
    for im in images:
        im = cv2.resize(im, (0, 0), None, 0.25, 0.25)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        encodeList = face_recognition.face_encodings(im)
        if(len(encodeList) != 0):
            encode = encodeList[0]
        encodings.append(encode)
    return encodings


def get_faces(frame):
    """
        Returns the faces of the people recognized on an image
    """
    resizedImage = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    resizedImage = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2RGB)
    webcamFaces = face_recognition.face_locations(resizedImage)
    webcamEncoding = face_recognition.face_encodings(resizedImage, webcamFaces)
    return webcamEncoding,webcamFaces


def get_matches(frame,knownEncodings,users):
    """
        Returns the identities of the people recognized on an image
    """
    webcamEncoding,webcamFaces = get_faces(frame)
    names = []

    for encodedFace, faceLocation in zip(webcamEncoding, webcamFaces):
        matches = face_recognition.compare_faces(knownEncodings, encodedFace)
        faceDistances = face_recognition.face_distance(knownEncodings, encodedFace)       
        matchId = np.argmin(faceDistances)

        if matches[matchId]:
            name = users[matchId]["name"]
            if users[matchId]["_id"] not in recognizedFaces:
                names.append(name)
                recognizedFaces.append(users[matchId]["_id"])
                
            y1, x2, y2, x1 = faceLocation
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,255,255), 4)
            cv2.rectangle(frame, (x1, y2-35), (x2, y2), (0, 0, 255,255), cv2.FILLED)
            cv2.putText(img=frame, text=name, org=(x1+6, y2-6),fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=1, color=[255,255,255,255], lineType=cv2.LINE_AA, thickness=2)
    
    return frame,names

def get_faces_frame(frame):
    """
        Returns a frame with squares around all faces
    """
    webcamEncoding,webcamFaces = get_faces(frame)
    if len(webcamFaces) > 0:
        y1, x2, y2, x1 = webcamFaces[0]
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,255,255), 4)
    return frame,webcamEncoding

