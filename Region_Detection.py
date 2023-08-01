# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 12:04:29 2023

@author: maena
"""
import cv2
from Region_Dictionary import Region,Origin_X,Origin_Y
import time
import numpy as np
import math
from picamera2 import Picamera2
#*********************************************
def picture_transform(frame):
    roi =np.zeros(frame.shape[:2],np.uint8)
    roi =cv2.circle(roi, (50,43),49,255,cv2.FILLED)
    mask=np.ones_like(frame)*255
    mask=(cv2.bitwise_and(mask, frame, mask=roi) +cv2.bitwise_and(mask,mask,mask=~roi))
    frame=cv2.medianBlur(mask,3)
    return frame
#*********************************************
def rectangle_coords(x,y,size):
    sizee=int(size/2)
    x=x-sizee
    y=y-sizee
    rect_list=[]
    for i in range(int(size)):
      for j in range(int(size)):
        rect_list.append((x+i,y+j))
    return rect_list
#*********************************************
def Move_Hexxy_JR(Curr_Region,SerialObj,Ball_Tracking,Error_List,piCam):
    Start_Time=time.time()
    Ball_Coords=Ball_Tracking[-1]
    Target=Region[Curr_Region]["Target"]
    P_Gain=Region[Curr_Region]["P Gain"]
    I_Gain=Region[Curr_Region]["I Gain"]
    D_Gain=Region[Curr_Region]["D Gain"]
    Error=math.sqrt(((Ball_Coords[0]-Target[0])**2)+((Ball_Coords[1]-Target[1])**2))
    I_Sum=0
    counter=0
    while(Error>5):
        Current_Time=time.time()
        Elapse_Time=Current_Time-Start_Time+1
        frame=piCam.capture_array()
        frame=picture_transform(frame)
        #cv2.imshow('Original',frame)
        Ball_Current_Location=Ball_detection(frame,Ball_Tracking)
        Ball_Coords=Ball_Tracking[-1]
        Error=math.sqrt(((Ball_Coords[0]-Target[0])**2)+((Ball_Coords[1]-Target[1])**2))
        Error_List.append(Error)
        Diff_Error=Error_List[-1]-Error_List[-2]
        print(Curr_Region)
#         print("Error")
#         print(Error)
#         print("Error Sum")
#         print(sum(Error_List))
#         print("Error Diff")
#         print(Diff_Error)
#         print("PID Value")
#         print(((Error*P_Gain)+(sum(Error_List)*I_Gain)+(Diff_Error*D_Gain)))
#         print("***************")
        Tilt_X=Region[Curr_Region]["X_pos"]*((Error*P_Gain)+(sum(Error_List)*I_Gain)+(Diff_Error*D_Gain))
        Tilt_Y=Region[Curr_Region]["Y_pos"]*((Error*P_Gain)++(sum(Error_List)*I_Gain)+(Diff_Error*D_Gain))
        if(Ball_Current_Location!=0):
            if(Region_Detection(Ball_Current_Location,frame)!=Curr_Region):
#                 print('coord')
#                 print(Area)
#                 print('measured reg')
#                 print(Region_Detection(Area,frame))
#                 print('curr')
#                 print(Curr_Region)
#                 print("Middel Change")
                break
        else:
            break
#         if(len(set(Ball_Tracking))<4 and len(Ball_Tracking)>9):
#             print("Stuck")
#             for i in Region[Curr_Region]["Stuck"]:
#                 Tilt_X_off=i[0]
#                 Tilt_Y_off=i[1]
#                 SerialObj.write(('MOV U '+str(Tilt_X_off)+' V '+str(Tilt_Y_off)+'\n').encode('ascii'))
#                 for i in range(20):
#                     frame=piCam.capture_array()
#                     frame=picture_transform(frame)
#                     cv2.imshow('Original',frame)
#                     Area=Ball_detection(frame,Ball_Tracking)
#                     if(Area!=0):
#                         if(Region_Detection(Area,frame)!=Curr_Region):
#                             print("Middel Change")
#                             return
#                     time.sleep(.05)
#             Ball_Tracking=[Ball_Tracking[-1]]
#             continue
        SerialObj.write(('VMO? U '+str(Tilt_X)+' V '+str(Tilt_Y)+'\n').encode('ascii'))
        Can_Move_There=SerialObj.readline()
#         print(Can_Move_There.decode())
        if(int(Can_Move_There.decode())==1):
            SerialObj.write(('MOV U '+str(Tilt_X)+' V '+str(Tilt_Y)+'\n').encode('ascii'))
        End_Time=time.time()
#         print(End_Time-Start_Time)

        
#*********************************************
def Region_Detection(Ball_Local,frame):
    for reg in Region:
        Curr_X=Ball_Local[0]-Origin_X
        Curr_Y=Ball_Local[1]-Origin_Y
        Curr_Angle=-1*(((math.atan2(Curr_Y,Curr_X)+math.pi)*180/math.pi)-360)
        #print('*****************')
        Curr_Radius=math.sqrt((Curr_X**2)+(Curr_Y**2))
        #print(Curr_X,Curr_Y,Curr_Angle,Curr_Radius)
        Region_IR=Region[reg]["Area"][0]
        Region_OR=Region[reg]["Area"][1]
        Region_MinA=Region[reg]["Area"][2]
        Region_MaxA=Region[reg]["Area"][3]
        #print(Region_IR,Region_OR,Region_MinA,Region_MaxA)
        #print('*****************')
        if(Curr_Radius>=Region_IR and Curr_Radius<=Region_OR):
            if(Curr_Angle>=Region_MinA and Curr_Angle<=Region_MaxA):
                return reg
    return 0
    #cv2.imshow('Original',frame)
#*********************************************
def Ball_detection(frame,Ball_Tracking):
    into_hsv =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    L_limit=np.array([59,162,0]) # setting the Green Balllower limit
    U_limit=np.array([139,255,183]) # setting the Green Ball upper limit
    b_mask=cv2.inRange(into_hsv,L_limit,U_limit)
    contours,_=cv2.findContours(b_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #print(len(contours))
    for cnt in contours:
        areas=cv2.contourArea(cnt)
        if (areas>200 and areas<1400): # will change depending on the distance of the image
            x,y,w,h=cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            cv2.putText(frame,("Ball"),(x,y-10),cv2.FONT_HERSHEY_PLAIN,5,(255,0,0))
            if len(Ball_Tracking)<10:
                Ball_Tracking.append((x,y))
            else:
                Ball_Tracking.pop(0)
                Ball_Tracking.append((x,y))
            #print(Ball_Tracking)
            x=int(x+(w/2))
            y=int(y+(h/2))
#             print(x,y)
            Ball_Current_Location=(x,y)
            frame[y][x]=(255,255,255)
            frame[y+1][x]=(255,255,255)
            frame[y-1][x]=(255,255,255)
            frame[y][x+1]=(255,255,255)
            frame[y+1][x+1]=(255,255,255)
            frame[y-1][x+1]=(255,255,255)
            frame[y][x-1]=(255,255,255)
            frame[y+1][x-1]=(255,255,255)
            frame[y-1][x-1]=(255,255,255)
            return Ball_Current_Location
    return 0
