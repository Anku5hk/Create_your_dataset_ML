import cv2
import numpy as np
import argparse
import os
import shutil

"""
Description:
    Save Face Images using your Webcam to the current directory only if face is detected. Image is saved by 2 methods
    1. By clicking anywhere in cv2s window(Default) 
    2. Automatically after 2 seconds if the argument is given.   
    The defalt method is using cv2s Harcascades change the code to try with something else.
Arguments:
    --full_frame(bool): save full frame of image. 
    --auto(bool): Auto click photos after 2 seconds.

"""

parser = argparse.ArgumentParser()
parser.add_argument('--full_frame', help="save full frame containing face", default=False, type=bool)
parser.add_argument('--auto', help="Auto click photos after 2 seconds", default=False, type=bool)
args = parser.parse_args()

cap = cv2.VideoCapture(0)
_, frame = cap.read()

detector = cv2.CascadeClassifier(cv2.data.haarcascades + 
                                        "haarcascade_frontalface_default.xml")
click_yes = False
a=0
image_id = 0

def auto_click(frame,faces,a, full_frame):
    global image_id
    if a % 20 == 0:
        for i, (x,y,w,h) in enumerate(faces):
            if full_frame:
                face_name = "FullImage{0}.jpg".format(image_id)
                cv2.imwrite(face_name, frame)
                print('Image saved')
                image_id+=1
            else:    
                face = frame[y:y + h, x:x + w] 
                face_name = "Face{0}Image{1}.jpg".format(i, image_id)
                cv2.imwrite(face_name, face)
                print('Image saved')
                image_id+=1
            if i > 3: 
                break


def point(event,x,y,flags,params):
    global click_yes 
    if event == cv2.EVENT_LBUTTONDBLCLK:
        click_yes = True

cv2.namedWindow("camera")
cv2.setMouseCallback("camera", point)      

while True:   
    ret, frame = cap.read()
    image = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=2, minSize=(25, 25))
    for i, (x,y,w,h) in enumerate(faces):
        cv2.rectangle(image, (x, y), (x+w, y+h), (0,0,255), 2)
        if i > 3:
            break

    if args.auto and len(faces) != 0:
        a+=1
        auto_click(frame,faces, a, args.full_frame)

    if click_yes and len(faces) != 0:    
        a+=1    
        for i, (x,y,w,h) in enumerate(faces):
            face_name = "FaceImage{0}.jpg".format(image_id)
            if args.full_frame:
                cv2.imwrite(face_name, frame)
                print('Image saved')
                image_id+=1
            else:    
                face = frame[y:y + h, x:x + w]  
                cv2.imwrite(face_name, face)
                print('Image saved')
                image_id+=1
            click_yes = False
            if i > 3: 
                break

                
    cv2.imshow('camera',image)
    key = cv2.waitKey(1)
    if key == 27:
        print("Total {0} Images Saved.".format(image_id))
        break

cap.release()
cv2.destroyAllWindows()

