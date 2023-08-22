import cv2
from threading import Thread
import argparse
from picamera2 import Picamera2
import numpy as np
import time
'''
Input: Raw Frame
Output: Filtered Frame
Description: Crops, Blurs, and filters the frame to get a black photo with contours (usually 1, the ball)
'''
def picture_transform(frame):
    frame=frame[0:100,13:112] #crops the frame so its smaller
    frame=cv2.medianBlur(frame,5) # Blurs the frame using Median BLur of a 5x5 Kernel
    roi =np.zeros(frame.shape[:2],np.uint8)
    roi =cv2.circle(roi,(53,46),46,255,cv2.FILLED)# Creates a circle around the maze (can ajust the (53,46)(*the origin*) and 47 (*Radius Length*)
    mask=np.ones_like(frame)*255 # A frame that is all white
    bounded_Region=(cv2.bitwise_and(mask, frame, mask=roi) +cv2.bitwise_and(mask,mask,mask=~roi)) #Takes the circle are and puts it on the white back ground 
    #Note: the image is already in grayscale
    bounded_Region=cv2.inRange(bounded_Region,0,70)# Takes anything that is 0-70 in grayscale color and turns it white while everything else is black, making contours
    return bounded_Region
'''
Input: Raw Frame
Output: Filtered Frame
Description: Crops and Blurs frame to get a viewable picture of the frame, only used in debugging
'''
def semi_picture_transform(frame):
    frame=frame[0:100,13:112] #crops the frame so its smaller
    frame=cv2.medianBlur(frame,5) # Blurs the frame using Median BLur of a 5x5 Kernel
    roi =np.zeros(frame.shape[:2],np.uint8) 
    roi =cv2.circle(roi, (53, 46),46,255,cv2.FILLED)# Creates a circle around the maze (can ajust the (53,46)(*the origin*) and 47 (*Radius Length*)
    mask=np.ones_like(frame)*255# A frame that is all white
    bounded_Region=(cv2.bitwise_and(mask, frame, mask=roi) +cv2.bitwise_and(mask,mask,mask=~roi))#Takes the circle are and puts it on the white back ground
    #Note: Does not filter out at the end like picture transform, this allows the user to still see the frame 
    return bounded_Region

'''
Description: A Class made for multithreading the Pi Camera
Note: This is using PICam2 and Raspbery Bulls Eye and a Picamera Module3 12MP 120 degree Wide Angle Lens, *******
Buy Camera with link: adafruit.com/product/5658
'''
class VideoGet:
    def __init__(self):
        self.piCam=Picamera2() # Initiating PiCam2
        self.piCam.preview_configuration.main.size=(150,100)# Initiating camera resolution to 150x100 pixel
        self.piCam.preview_configuration.main.format="YUV420"# Initialing Camera Config which is Gray scale 
        self.piCam.preview_configuration.controls.FrameRate=40 #Setting frame rate to 40 fps
        self.piCam.preview_configuration.align() #More nonsense to be initiated
        self.piCam.configure("preview") #sets camera to all the settings
        self.piCam.start() # starts video
        self.frame=picture_transform(self.piCam.capture_array()) # transforms the first frame to desired frame
        self.preserved_frame=semi_picture_transform(self.piCam.capture_array()) # Transforms to a viewable frame (only used in debugging)
        self.stopped = False #Variable used to stop video capture when True, set to False on initation
    def start(self):
        Thread(target=self.get,daemon=True, args=()).start() #Starts the multithreading, using Daemon
        return self
    
    def get(self):
        while not self.stopped: #Continues to collect image frames unti self.stop is True
            self.frame=picture_transform(self.piCam.capture_array())# transforms the first frame to desired frame
            self.preserved_frame=semi_picture_transform(self.piCam.capture_array()[:100,:150])# Transforms to a viewable frame (only used in debugging)
        return
    def stop(self):
        self.stopped = True #Sets Stopped to true, stopping the frame collecting loop
        self.piCam.stop_preview() # Stops the Picam
        self.piCam.close() # CLoses PICam
        #Stopping and CLosing allow the PI to create a new thread afterwards if needed


