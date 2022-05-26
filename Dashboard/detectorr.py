import cv2
import os
# import sqlite3
import numpy as np
from PIL import Image
from django.conf import settings
from .E_Attendance import *

detector = cv2.CascadeClassifier(str(settings.BASE_DIR)  + '/Dashboard/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

class Face_authentication:

   # face detection from the webcam

    def Detectfaces(self, Entry, ):
        face_id = Entry
        cap = cv2.VideoCapture(0)

        count = 0

        while (True):

            success, img = cap.read()
            # img = cv2.flip(img, -1) # flip video image vertically
            cvt_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(cvt_img, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1

                # Save the captured image into the datasets folder
                cv2.imwrite(str(settings.BASE_DIR) + '/Dashboard/dataset/User.' + str(face_id) + '.' + str(count) + ".jpg",
                            cvt_img[y:y + h, x:x + w])

                cv2.imshow('Register Face', img)

            k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 30:  # Take 30 face sample and stop video
                break

        cap.release()
        cv2.destroyAllWindows()

    # train the images

    def traindata(self):
        # Path for face image database
        path = str(settings.BASE_DIR) + '/Dashboard/dataset'

        # get images and label data
        def getImagesAndLabels(path):

            Paths = [os.path.join(path, f) for f in os.listdir(path)]
            Samples = []
            ids = []

            for Path in Paths:

                PIL_img = Image.open(Path).convert('L')  # convert it to grayscale
                img_numpy = np.array(PIL_img, 'uint8')

                face_id = int(os.path.split(Path)[-1].split(".")[1])
                print("face_id", face_id)
                faces = detector.detectMultiScale(img_numpy)

                for (x, y, w, h) in faces:
                    Samples.append(img_numpy[y:y + h, x:x + w])
                    ids.append(face_id)

            return Samples, ids

        print("\n Training faces. It will take a few seconds. Wait ...")
        faces, ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        recognizer.save(
            str(settings.BASE_DIR)  + '/Dashboard/trainer/trainer.yml')  # recognizer.save() worked on Mac, but not on Pi

        # Print the numer of faces trained and end program
        print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))

    # recognize face

    def recognizeFace(self):
        recognizer.read(str(settings.BASE_DIR) + '/Dashboard/trainer/trainer.yml')
        cascadePath = str(settings.BASE_DIR)  + '/Dashboard/haarcascade_frontalface_default.xml'
        faceCascade = cv2.CascadeClassifier(cascadePath)

        font = cv2.FONT_HERSHEY_SIMPLEX

        confidence = 0
        cam = cv2.VideoCapture(0)

        # Define min window size to be recognized as a face
        minWidth = 0.1 * cam.get(3)
        minHeight = 0.1 * cam.get(4)

        while True:

            ret, img = cam.read()

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minWidth), int(minHeight)),
            )

            for (x, y, w, h) in faces:

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                face_id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                # Check if confidence is less then 100 ==> "0" is perfect match
                if (confidence < 20):
                    name = 'Detected'
                else:
                    name = "Unknown"

                cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

            cv2.imshow('Detect Face', img)

            k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break
            if confidence > 50:
                break

         #mark_attendance

        markAttendance(str(face_id))
        print("\n Exiting Program")
        cam.release()
        cv2.destroyAllWindows()
        print(face_id)
        return face_id

