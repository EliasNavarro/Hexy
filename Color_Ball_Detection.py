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
from Region_Detection import Region_Detection,Ball_detection,Move_Hexxy_JR,picture_transform
convert=math.pi/180
from picamera2 import Picamera2
from Camera import VideoGet

#*****************************************
offset_X=97
offset_Y=89
ring1_1=create_region((offset_X,offset_Y),80,96,82,95)
ring1_2=create_region((offset_X,offset_Y),82,96,93,195) #2 degree overlap
ring1_3=create_region((458, 469),269,308,87,184) #5 degree overlap
ring1_4=create_region((458, 469),269,308,-3,87)  #5 degree overlap
ring1_5=create_region((offset_X,offset_Y),82,96,0,84)  #2 degree overlap

ring2_1=create_region((308, 252),155,200,-25,26)
ring2_2=create_region((308, 252),155,200,225,340)
ring2_3=create_region((308, 252),155,200,202,230)
ring2_4=create_region((308, 252),155,200,110,210)
ring2_5=create_region((308, 252),155,200,40,110)

ring3_1=create_region((308, 252),113,150,-40,23)
ring3_2=create_region((308, 252),113,150,240,320)
ring3_3=create_region((308, 252),113,150,140,245)
ring3_4=create_region((308, 252),113,150,105,145)
ring3_5=create_region((308, 252),113,150,43,110)
# 
# ring4_1=create_region((308, 252),78,103,198,225)
# ring4_2=create_region((308, 252),78,103,125,192)
# ring4_3=create_region((308, 252),78,103,-5,123)
# ring4_4=create_region((308, 252),78,103,-45,-5)
# ring4_5=create_region((308, 252),78,103,-97,-45)
# ring5_1=create_region((308, 252),0,50,0,360)
ramp=create_region((458,469),80,279,-7,4)
#************************************************
SerialObj = serial.Serial('/dev/ttyUSB0', 115200, timeout=30, parity=serial.PARITY_EVEN, rtscts=1)# COMxx   format on Windows
SerialObj.baudrate = 115200  # set Baud rate to 9600
SerialObj.bytesize = 8     # Number of data bits = 8
SerialObj.parity   ='N'    # No parity
SerialObj.stopbits = 1     # Number of Stop bits = 1
SerialObj.write(b'VLS 20\n')
#************************************************* 
Ball_Tracking=[]
Prev_Region="Deez Nuts"
video_getter = VideoGet().start()
cap1=1
Error_List=[0]
while (True):
    #frame=piCam.capture_array()
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
                    Error_List=[0]
                #print(Current_Region)
                Move_Hexxy_JR(Current_Region,SerialObj,Ball_Tracking,Error_List,video_getter)
                Prev_Region=Current_Region
            else:
                print()#"No Location G")
        else:
            print("no ballz")
        #cv2.imshow('Original',frame)
        
        if cv2.waitKey(1)==27:
            Maze=P_frame
            video_getter.stop()
            break
    else:
        Maze=frame
        break
# cap.release()
cv2.destroyAllWindows()
im = Maze
# Create figure and axes
fig, ax = plt.subplots()
# Dispay the image
ax.imshow(im)
# Create a Rectangle patch

rect = patches.Circle((97, 89),96, linewidth=1, edgecolor='r', facecolor='none')
# rect2 = patches.Circle((307, 243), 215, linewidth=1, edgecolor='r', facecolor='none')
# rect3 = patches.Circle((307, 243), 165, linewidth=1, edgecolor='r', facecolor='none')
# rect4 = patches.Circle((307, 243), 115, linewidth=1, edgecolor='r', facecolor='none')
# rect5 = patches.Circle((307, 243), 65, linewidth=1, edgecolor='r', facecolor='none')
# Add the patch to the Axes
ax.add_patch(rect)
# ax.add_patch(rect2)
# ax.add_patch(rect3)
# ax.add_patch(rect4)
# ax.add_patch(rect5)


#plt.plot([item[0] for item in Ball_Location], [item[1] for item in Ball_Location])
plt.scatter([item[0] for item in ring1_1], [item[1] for item in ring1_1])
plt.scatter([item[0] for item in ring1_2], [item[1] for item in ring1_2])
# plt.scatter([item[0] for item in ring1_3], [item[1] for item in ring1_3],s=.5)
# plt.scatter([item[0] for item in ring1_4], [item[1] for item in ring1_4],s=.5)
plt.scatter([item[0] for item in ring1_5], [item[1] for item in ring1_5])
plt.scatter(int(89*math.cos(-88*convert)+97),int(89*math.sin(-88*convert)+89),s=8)
plt.scatter(int(70*math.cos(-88*convert)+97),int(70*math.sin(-88*convert)+89),s=8)
# plt.scatter(int(300*math.cos(-1*convert)+458),int(300*math.sin(-1*convert)+469),s=4)
# plt.scatter([item[0] for item in ring2_1], [item[1] for item in ring2_1],s=.5)
# plt.scatter([item[0] for item in ring2_2], [item[1] for item in ring2_2],s=.5)
# plt.scatter([item[0] for item in ring2_3], [item[1] for item in ring2_3],s=.5)
# plt.scatter([item[0] for item in ring2_4], [item[1] for item in ring2_4],s=.5)
# plt.scatter([item[0] for item in ring2_5], [item[1] for item in ring2_5],s=.5)
# plt.scatter(int(175*math.cos(219*convert)+308),int(175*math.sin(219*convert)+252),s=4)
# plt.scatter(int(135*math.cos(219*convert)+308),int(135*math.sin(219*convert)+252),s=4)
# plt.scatter([item[0] for item in ring3_1], [item[1] for item in ring3_1],s=.5)
# plt.scatter([item[0] for item in ring3_2], [item[1] for item in ring3_2],s=.5)
# plt.scatter([item[0] for item in ring3_3], [item[1] for item in ring3_3],s=.5)
# plt.scatter([item[0] for item in ring3_4], [item[1] for item in ring3_4],s=.5)
# plt.scatter([item[0] for item in ring3_5], [item[1] for item in ring3_5],s=.5)
# plt.scatter(int(132*math.cos(125*convert)+308),int(132*math.sin(125*convert)+252),s=4)
# plt.scatter(int(85*math.cos(125*convert)+308),int(85*math.sin(125*convert)+252),s=4)

# plt.scatter([item[0] for item in ring4_1], [item[1] for item in ring4_1],s=.5)
# plt.scatter([item[0] for item in ring4_2], [item[1] for item in ring4_2],s=.5)
# plt.scatter([item[0] for item in ring4_3], [item[1] for item in ring4_3],s=.5)
# plt.scatter([item[0] for item in ring4_4], [item[1] for item in ring4_4],s=.5)
# plt.scatter([item[0] for item in ring4_5], [item[1] for item in ring4_5],s=.5)
# plt.scatter([item[0] for item in ring5_1], [item[1] for item in ring5_1],s=.5)
# plt.scatter([item[0] for item in ramp], [item[1] for item in ramp],s=.5)
plt.show()
SerialObj.write(('MOV U '+str(0)+' V '+str(0)+'\n').encode('ascii'))
SerialObj.close()

