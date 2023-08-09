import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import math
import serial
import time
from create_region import create_region
from Region_Dictionary import Region
from Region_Detection import Region_Detection,Ball_detection,Move_Hexxy_JR
convert=math.pi/180
from picamera2 import Picamera2
from Camera import VideoGet

#*****************************************
offset_X=53
offset_Y=46
ring1_1=create_region((offset_X,offset_Y),38,47,82,97)
ring1_2=create_region((offset_X,offset_Y),40,47,94,195) #2 degree overlap
ring1_3=create_region((offset_X,offset_Y),40,47,193,270) #5 degree overlap
ring1_4=create_region((offset_X,offset_Y),40,47,270,360)  #5 degree overlap
ring1_5=create_region((offset_X,offset_Y),40,47,0,84)  #2 degree overlap

ring2_1=create_region((offset_X,offset_Y),30,38,6,80)
ring2_2=create_region((offset_X,offset_Y),30,39,80,169)
ring2_3=create_region((offset_X,offset_Y),29,39,167,190)
ring2_4=create_region((offset_X,offset_Y),31,39,189,300)
ring2_5=create_region((offset_X,offset_Y),31,39,300,353)

ring3_1=create_region((offset_X,offset_Y),21,29,6,80)
ring3_2=create_region((offset_X,offset_Y),21,29,80,166)
ring3_3=create_region((offset_X,offset_Y),21,29,166,260)
ring3_4=create_region((offset_X,offset_Y),21,29,259,288)
ring3_5=create_region((offset_X,offset_Y),21,29,288,349)
# 
ring4_1=create_region((offset_X,offset_Y),14,21,294,348)
ring4_2=create_region((offset_X,offset_Y),14,21,200,294)
ring4_3=create_region((offset_X,offset_Y),14,20,110,200)
ring4_4=create_region((offset_X,offset_Y),12,20,70,110)
ring4_5=create_region((offset_X,offset_Y),13,20,18,70)

ring5_1=create_region((offset_X,offset_Y),0,12,0,360)
ramp1=create_region((offset_X,offset_Y),10,40,0,4)
ramp2=create_region((offset_X,offset_Y),10,40,356,360)
#************************************************
SerialObj = serial.Serial('/dev/ttyUSB0', 115200, timeout=30, parity=serial.PARITY_EVEN, rtscts=1)# COMxx   format on Windows
SerialObj.baudrate = 115200  # set Baud rate to 9600
SerialObj.bytesize = 8     # Number of data bits = 8
SerialObj.parity   ='N'    # No parity
SerialObj.stopbits = 1     # Number of Stop bits = 1
SerialObj.write(b'VLS 13\n')
#************************************************* 
Ball_Tracking=[(0,0)]
Prev_Region="Deez Nuts"
video_getter = VideoGet().start()
cap1=1
Error_List=[0,0]
while (True):
    frame = video_getter.frame
    P_frame=video_getter.preserved_frame
    ret=True
    if ret==True:
        if cap1==1:
            Maze=P_frame
            cap1=0
            #cv2.imwrite('poopoopeepee.jpg',frame)
            #video_getter.stop()
            #break
        Ball_Location=Ball_detection(frame,Ball_Tracking)
        #print(Ball_Location)
        if(Ball_Location!=0):
            Current_Region=Region_Detection(Ball_Location,frame)
            if(Current_Region!=0):
                if(Current_Region[4]!=Prev_Region[4]):
                    Ball_Tracking=[(0,0)]
                    Error_List=[0,0]
                print(Current_Region)
                Move_Hexxy_JR(Current_Region,SerialObj,Ball_Tracking,Error_List,video_getter)
                Prev_Region=Current_Region
            else:
                joe=5
                #print("No Location G")
            print()
        else:
            print("no ballz")
        #cv2.imshow('Original',frame)
        
        if cv2.waitKey(1)==27:
            Maze=frame
            video_getter.stop()
            break
    else:
        Maze=frame
        break
cv2.destroyAllWindows()
im = Maze
fig, ax = plt.subplots()
ax.imshow(im)

rect = patches.Circle((50,50),47, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)

#plt.plot([item[0] for item in Ball_Location], [item[1] for item in Ball_Location])
# plt.scatter([item[0] for item in ring1_1], [item[1] for item in ring1_1])
# plt.scatter([item[0] for item in ring1_2], [item[1] for item in ring1_2])
# plt.scatter([item[0] for item in ring1_3], [item[1] for item in ring1_3])
# plt.scatter([item[0] for item in ring1_4], [item[1] for item in ring1_4])
# plt.scatter([item[0] for item in ring1_5], [item[1] for item in ring1_5])
# plt.scatter(int(47*math.cos(-89*convert)+50),int(47*math.sin(-89*convert)+50),s=8)
# plt.scatter(int(30*math.cos(-89*convert)+50),int(30*math.sin(-89*convert)+50),s=8)
# plt.scatter(int(47*math.cos(0*convert)+50),int(47*math.sin(0*convert)+50),s=8)
# plt.scatter([item[0] for item in ring2_1], [item[1] for item in ring2_1])
# plt.scatter([item[0] for item in ring2_2], [item[1] for item in ring2_2])
# plt.scatter([item[0] for item in ring2_3], [item[1] for item in ring2_3])
# plt.scatter([item[0] for item in ring2_4], [item[1] for item in ring2_4])
# plt.scatter([item[0] for item in ring2_5], [item[1] for item in ring2_5])
# plt.scatter(int(38*math.cos(-178*convert)+50),int(38*math.sin(-178*convert)+50),s=8)
# plt.scatter(int(22*math.cos(-178*convert)+50),int(22*math.sin(-178*convert)+50),s=8)
# plt.scatter([item[0] for item in ring3_1], [item[1] for item in ring3_1])
# plt.scatter([item[0] for item in ring3_2], [item[1] for item in ring3_2])
# plt.scatter([item[0] for item in ring3_3], [item[1] for item in ring3_3])
# plt.scatter([item[0] for item in ring3_4], [item[1] for item in ring3_4])
# plt.scatter([item[0] for item in ring3_5], [item[1] for item in ring3_5])
# plt.scatter(int(29*math.cos(-273*convert)+50),int(29*math.sin(-273*convert)+50),s=8)
# plt.scatter(int(12*math.cos(-273*convert)+50),int(12*math.sin(-273*convert)+50),s=4)
plt.scatter([item[0] for item in ring4_1], [item[1] for item in ring4_1])
plt.scatter([item[0] for item in ring4_2], [item[1] for item in ring4_2])
plt.scatter([item[0] for item in ring4_3], [item[1] for item in ring4_3])
plt.scatter([item[0] for item in ring4_4], [item[1] for item in ring4_4])
plt.scatter([item[0] for item in ring4_5], [item[1] for item in ring4_5])
plt.scatter(int(20*math.cos(-90*convert)+50),int(20*math.sin(-90*convert)+50),s=4)
plt.scatter(int(0*math.cos(-90*convert)+50),int(0*math.sin(-90*convert)+50),s=4)
plt.scatter([item[0] for item in ring5_1], [item[1] for item in ring5_1])
plt.scatter([item[0] for item in ramp1], [item[1] for item in ramp1])
plt.scatter([item[0] for item in ramp2], [item[1] for item in ramp2])
plt.show()
SerialObj.write(('MOV U '+str(0)+' V '+str(0)+'\n').encode('ascii'))
SerialObj.close()

