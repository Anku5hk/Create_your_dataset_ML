import cv2
import re
import shutil
import os 
import argparse
"""
Description:
    Automatically Save Face Images from current directory images to /extracted. Just run this .py in the required directory.
    The defalt method is using cv2s Harcascades change the code to try with something else.
"""

imgs_dir = os.curdir
if os.path.isdir(imgs_dir + 'extracted_faces/'):
    pass
else:
    os.mkdir(imgs_dir + 'extracted_faces/')

imgs = os.listdir(imgs_dir)

pat1 = r'(\w+)\.jpg'
pat2 = r'(\w+)\.png'

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 
                            "haarcascade_frontalface_default.xml")
total_faces = 0
for img in imgs:  
  
    pat_str1 = re.search(pat1, img)
    pat_str2 = re.search(pat2, img)
    if pat_str1:
        img =  pat_str1.group(1)
    elif pat_str2:
        img =  pat_str2.group(1)    
    else:
        continue

    image = cv2.imread(imgs_dir + img + '.jpg')
    faces = faceCascade.detectMultiScale(
            image,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
    )
    if len(faces) != 0:
        for i, (x, y, w, h) in enumerate(faces):
            roi_color = image[y:y + h, x:x + w] 
            face_name = img +'_face'+str(i)+'.jpg'    
            cv2.imwrite(face_name, roi_color)
            save_loc = os.path.realpath(imgs_dir + "extracted_faces/" + face_name)
            from_loc = os.path.realpath(imgs_dir + face_name)
            shutil.move(from_loc,save_loc) 
            total_faces+=1
print('DONE')

