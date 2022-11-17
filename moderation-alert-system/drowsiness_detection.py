import cv2
import os
from keras.models import load_model
import numpy as np
from pygame import mixer
import time

from PIL import Image
from numpy import asarray


face = cv2.CascadeClassifier('haarcascadefiles/haarcascade_frontalface_alt.xml')
leye = cv2.CascadeClassifier('haarcascadefiles/haarcascade_lefteye_2splits.xml')
reye = cv2.CascadeClassifier('haarcascadefiles/haarcascade_righteye_2splits.xml')

lbl=['Close','Open']
model = load_model('models/cnncat2.h5')
def isDrowsy(image_path):
    img = Image.open(image_path) 
    frame = asarray(img)
    count=0
    rpred=[99]
    lpred=[99]

    height,width = frame.shape[:2] 

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face.detectMultiScale(gray,minNeighbors=5,scaleFactor=1.1,minSize=(25,25))
    left_eye = leye.detectMultiScale(gray)
    right_eye =  reye.detectMultiScale(gray)

    cv2.rectangle(frame, (0,height-50) , (200,height) , (0,0,0) , thickness=cv2.FILLED )

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y) , (x+w,y+h) , (100,100,100) , 1 )

    for (x,y,w,h) in right_eye:
        r_eye=frame[y:y+h,x:x+w]
        count=count+1
        r_eye = cv2.cvtColor(r_eye,cv2.COLOR_BGR2GRAY)
        r_eye = cv2.resize(r_eye,(24,24))
        r_eye= r_eye/255
        r_eye=  r_eye.reshape(24,24,-1)
        r_eye = np.expand_dims(r_eye,axis=0)
        y_pred = model.predict(r_eye)
        rpred=np.argmax(y_pred,axis=1)
        if(rpred[0]==1):
            lbl='Open' 
        if(rpred[0]==0):
            lbl='Closed'
        break

    for (x,y,w,h) in left_eye:
        l_eye=frame[y:y+h,x:x+w]
        count=count+1
        l_eye = cv2.cvtColor(l_eye,cv2.COLOR_BGR2GRAY)  
        l_eye = cv2.resize(l_eye,(24,24))
        l_eye= l_eye/255
        l_eye=l_eye.reshape(24,24,-1)
        l_eye = np.expand_dims(l_eye,axis=0)
        y_pred = model.predict(l_eye)
        lpred=np.argmax(y_pred,axis=1)
        if(lpred[0]==1):
            lbl='Open'   
        if(lpred[0]==0):
            lbl='Closed'
        break

    if(rpred[0]==0 and lpred[0]==0):
        return 1#closed
    else:
        return 0#open

        