# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 08:20:19 2023

@author: maena
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 17:42:42 2023

@author: Elias
"""

import cv2
from threading import Thread
import argparse
from picamera2 import Picamera2
import numpy as np
import time

def picture_transform(frame):
    frame=frame[0:100,13:112]
    frame=cv2.medianBlur(frame,5)
    roi =np.zeros(frame.shape[:2],np.uint8)
    roi =cv2.circle(roi,(53,46),47,255,cv2.FILLED)
    mask=np.ones_like(frame)*255
    bounded_Region=(cv2.bitwise_and(mask, frame, mask=roi) +cv2.bitwise_and(mask,mask,mask=~roi))
    #bounded_Region=cv2.resize(bounded_Region,(300,300))
    bounded_Region=cv2.inRange(bounded_Region,0,55)
    return bounded_Region
def semi_picture_transform(frame):
    frame=frame[0:100,13:112]
    #frame=cv2.medianBlur(frame,5)
    roi =np.zeros(frame.shape[:2],np.uint8)
    roi =cv2.circle(roi, (53, 46),47,255,cv2.FILLED)
    mask=np.ones_like(frame)*255
    bounded_Region=(cv2.bitwise_and(mask, frame, mask=roi) +cv2.bitwise_and(mask,mask,mask=~roi))
    #bounded_Region=cv2.cvtColor(bounded_Region,cv2.COLOR_BGR2GRAY)
    return bounded_Region
class VideoGet:
    def __init__(self):
        self.piCam=Picamera2()
        self.piCam.preview_configuration.main.size=(150,100)#(1280,720)
        self.piCam.preview_configuration.main.format="YUV420"#"RGB888"
        self.piCam.preview_configuration.controls.FrameRate=40
        self.piCam.preview_configuration.align()
        self.piCam.configure("preview")
        self.piCam.start()
        self.frame=picture_transform(self.piCam.capture_array())#[:100,:100])
        self.preserved_frame=semi_picture_transform(self.piCam.capture_array())
        self.stopped = False
        
    def start(self):
        Thread(target=self.get,daemon=True, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            self.frame=picture_transform(self.piCam.capture_array())#self.piCam.capture_array()
            self.preserved_frame=semi_picture_transform(self.piCam.capture_array()[:100,:100])
    def stop(self):
        self.stopped = True

def threadVideoGet(source):
#     piCam=Picamera2()
#     piCam.preview_configuration.main.size=(100,100)
#     piCam.preview_configuration.main.format="RGB888"
#     piCam.preview_configuration.align()
#     piCam.preview_configuration.controls.FrameRate=25
#     piCam.configure("preview")
#     piCam.start()
    video_getter = VideoGet().start()
    while True:
        start=time.time()
        if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            cv2.destroyAllWindows()
            break
        #frame=piCam.capture_array()
        frame = video_getter.frame
        
        width=int(frame.shape[1]*3)
        height=int(frame.shape[0]*3)
        frame=cv2.resize(frame,(width,height),interpolation=cv2.INTER_AREA)
        
        end=time.time()
        #print(end-start)
#         contours,_=cv2.findContours(frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#         print(len(contours))
#         cv2.drawContours(frame,contours,-1,(0,255,0),3)
        cv2.imshow("Video", frame)
#threadVideoGet(0)
