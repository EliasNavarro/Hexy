# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 12:04:29 2023

@author: maena
"""
import cv2
from Region_Dictionary import Region
import time
import numpy as np
import math
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
def Move_Hexxy_JR(Curr_Region,SerialObj,cap,Ball_Tracking,Error_List):
    Start_Time=time.time()
    Ball_Coords=Ball_Tracking[-1]
    Target=Region[Curr_Region]["Target"]
    P_Gain=Region[Curr_Region]["P Gain"]
    I_Gain=Region[Curr_Region]["I Gain"]
    D_Gain=Region[Curr_Region]["D Gain"]
    Error=math.sqrt(((Ball_Coords[0]-Target[0])**2)+((Ball_Coords[1]-Target[1])**2))
    I_Sum=0
    counter=0
    while(Error>2):
        Current_Time=time.time()
        Elapse_Time=Current_Time-Start_Time+1
        ret,frame =cap.read()
        cv2.imshow('Original',frame)
        Area=Ball_detection(frame,Ball_Tracking)
        Ball_Coords=Ball_Tracking[-1]
        Error=math.sqrt(((Ball_Coords[0]-Target[0])**2)+((Ball_Coords[1]-Target[1])**2))
        Error_List.append(Error)
        Diff_Error=Error_List[-1]-Error_List[-2]
        print(Curr_Region)
        print("Error")
        print(Error)
        print("Error Sum")
        print(sum(Error_List))
        print("Error Diff")
        print(Diff_Error)
        print("PID Value")
        print(((Error*P_Gain)+(sum(Error_List)*I_Gain)+(Diff_Error*D_Gain)))
        print("***************")
        Tilt_X=Region[Curr_Region]["X_pos"]*((Error*P_Gain)+(sum(Error_List)*I_Gain)+(Diff_Error*D_Gain))
        Tilt_Y=Region[Curr_Region]["Y_pos"]*((Error*P_Gain)++(sum(Error_List)*I_Gain)+(Diff_Error*D_Gain))
        if(Area!=0):
            if(Region_Detection(Area,frame)!=Curr_Region):
                print("Middel Change")
                break
        else:
            break
        if(len(set(Ball_Tracking))<4 and len(Ball_Tracking)>9):
            print("Stuck")
            for i in Region[Curr_Region]["Stuck"]:
                Tilt_X_off=i[0]
                Tilt_Y_off=i[1]
                SerialObj.write(('MOV U '+str(Tilt_X_off)+' V '+str(Tilt_Y_off)+'\n').encode('ascii'))
                for i in range(20):
                    ret,frame =cap.read()
                    cv2.imshow('Original',frame)
                    Area=Ball_detection(frame,Ball_Tracking)
                    if(Area!=0):
                        if(Region_Detection(Area,frame)!=Curr_Region):
                            print("Middel Change")
                            return
                    time.sleep(.05)
            Ball_Tracking=[Ball_Tracking[-1]]
            continue
        SerialObj.write(('VMO? U '+str(Tilt_X)+' V '+str(Tilt_Y)+'\n').encode('ascii'))
        Can_Move_There=SerialObj.readline()  
        if(int(Can_Move_There.decode())==1):
            SerialObj.write(('MOV U '+str(Tilt_X)+' V '+str(Tilt_Y)+'\n').encode('ascii'))
#*********************************************
def Region_Detection(Area,frame):
    for i in Area:
        for reg in Region:
            for coordinates in Region[reg]["Area"]:
                if (abs(i[0]-coordinates[0])<3 and abs(i[1]-coordinates[1])<3):
                    return reg
    return 0
    #cv2.imshow('Original',frame)
#*********************************************
def Ball_detection(frame,Ball_Tracking):
    into_hsv =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    # L_limit=np.array([0,230,140]) # setting the Yellow Balllower limit
    # U_limit=np.array([85,255,255]) # setting the Yellow Ball upper limit
    L_limit=np.array([39,110,0]) # setting the Green Balllower limit
    U_limit=np.array([255,255,255]) # setting the Green Ball upper limit
    b_mask=cv2.inRange(into_hsv,L_limit,U_limit)
#     kernel=np.ones((40,40),np.uint8)
#     b_mask=cv2.morphologyEx(b_mask,cv2.MORPH_CLOSE,kernel)
    
    contours,_=cv2.findContours(b_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if (area>10 ):#and area<500): # will change depending on the distance of the image
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
            rect=[(x,y)]#rectangle_coords(x,y,5)
#             frame[y][x]=(255,255,255)
#             frame[y+1][x]=(255,255,255)
#             frame[y-1][x]=(255,255,255)
#             frame[y][x+1]=(255,255,255)
#             frame[y+1][x+1]=(255,255,255)
#             frame[y-1][x+1]=(255,255,255)
#             frame[y][x-1]=(255,255,255)
#             frame[y+1][x-1]=(255,255,255)
#             frame[y-1][x-1]=(255,255,255)
            #cv2.imshow('Original',frame)
            # cv2.imshow('Blue Detector',b_mask) # to display the blue object output
            return rect
    return 0
