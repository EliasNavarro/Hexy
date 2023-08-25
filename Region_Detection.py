import cv2
from Region_Dictionary import Region,Origin_X,Origin_Y
import time
import numpy as np
import math
from picamera2 import Picamera2
from PIJoystick import PIJoystick
from pipython.pidevice.gcsmessages import GCSMessages
from pipython.pidevice.gcscommands import GCSCommands
#*********************************************
'''
Input: Time elapsed/passed, Controller
Output: None
Description: Checks to see if the elapse time is more than 5, seconds, then it will move the Hexapod 
'''
def stuck(Time_Passed,c887):
    if(Time_Passed>5):
        c887.GcsCommandset('VLS 20')
        c887.GcsCommandset('MOV U 0 V 0')
        time.sleep(.5)
        c887.GcsCommandset('MOV U 0 V 5')
        time.sleep(.5)
        c887.GcsCommandset('MOV U 5 V 0')
        time.sleep(.5)
        c887.GcsCommandset('MOV U 0 V -5')
        time.sleep(.5)
        c887.GcsCommandset('MOV U 0-5 V 0')
        time.sleep(.5)
        c887.GcsCommandset('VLS 10')
        return True
    return False

#*********************************************
'''
Input: Balls Current Region, List of balls prevous location, A list of previus Error, Picamera Class, joystick class, controller signal
Output: None
Description: Moves the Hexapod depending on balls location and ends if the ball leaves the current region
'''
def Move_Hexxy_JR(Curr_Region,Ball_Tracking,Error_List,video_getter,joystick,c887):
    Start_Time=time.time() #Time Variable
    Ball_Coords=Ball_Tracking[-1] #Takes the most recent Ball tracking as the current location
    Target=Region[Curr_Region]["Target"] #calls the current Region's Target Position from Dictionary
    P_Gain=Region[Curr_Region]["P Gain"] #calls the current Region's P Value from Dictionary
    I_Gain=Region[Curr_Region]["I Gain"] #calls the current Region's I Value from Dictionary
    D_Gain=Region[Curr_Region]["D Gain"] #calls the current Region's D Value from Dictionary
    Error=math.sqrt(((Ball_Coords[0]-Target[0])**2)+((Ball_Coords[1]-Target[1])**2)) # Calculates the Error which is just the hypotenuse between the targets and current position
    start=time.time() #Start time when the loop begins
    while(Error>1): #Loops untill the ball is basically at the target but since the targets overlap the next region, the cycle continues
        if(joystick.read()[2]==1): # if the joystick button is pressed, just exits entirely
            return
        Elapse_Time=time.time()-start # calculates how long the balls been in the current region and in this loop
        frame = video_getter.frame # collects a frame from the camera
        Ball_Current_Location=Ball_detection(frame,Ball_Tracking)# uses the Ball detection and tracking to figure where the ball is currently
        Ball_Coords=Ball_Tracking[-1] # Gets the current location of ball
        n=.5 #ratio for low pass filter
        LP_Ball_Coords=[(Ball_Tracking[-2][0]*n)+(Ball_Tracking[-1][0]*(1-n)),(Ball_Tracking[-2][1]*n)+(Ball_Tracking[-1][1]*(1-n))]# gets low pass filter location which is just the mean of the current and last location
        LP_Error=math.sqrt(((LP_Ball_Coords[0]-Target[0])**2)+((LP_Ball_Coords[1]-Target[1])**2)) #Calculates the Error for the lowpass filter location from the target
        Error=math.sqrt(((Ball_Coords[0]-Target[0])**2)+((Ball_Coords[1]-Target[1])**2)) # Calculates the error with the actual location from the target
        Error_List.append(LP_Error) #Appends lowpass filter to error list (since only the D part of the PID use the error list we can do this)
        Diff_Error=Error_List[-1]-Error_List[-2] # computes the difference between the current error and the previous error
        Tilt_X=round(Region[Curr_Region]["X_pos"]*((Error*P_Gain)+((Elapse_Time**2)*I_Gain)+(Diff_Error*D_Gain)),1)# Takes the given regions X tilt and incorporates PID
        #Note: for I term, its just elapse time times squared times I term, it makes it so it doesn't effect the hexapod tilt untill 3-4 seconds
        Tilt_Y=round(Region[Curr_Region]["Y_pos"]*((Error*P_Gain)+((Elapse_Time**2)*I_Gain)+(Diff_Error*D_Gain)),1)# Takes the given regions Y tilt and incorporates PID
        if(Diff_Error>0): #If the Diff_Error is positive that means its going farther away from the target-> increase tilt which is sometimes too much so half the tilt 
            Tilt_X=Tilt_X/2
            Tilt_Y=Tilt_Y/2
        if(Curr_Region=="Ramp0_1" or Curr_Region=="Ramp0_2"or Curr_Region=="Ring5_1" or Curr_Region == "Ring1_1"or Curr_Region == "Ring4_4"or Curr_Region == "Ring3_4"):
            #This if statment just takes all of the regions with opening/ramp/goals, and ignores PID by tilting the Hexapod fully, The PID doesn't help these regions anyways
            Tilt_X=Region[Curr_Region]["X_pos"]
            Tilt_Y=Region[Curr_Region]["Y_pos"]
        if(Ball_Current_Location!=0): # checks to make sure the ball is still detectable
            if(Region_Detection(Ball_Current_Location)!=Curr_Region): #If the ball is in a different region than it started, will exit this function
                break
        else: # if the ball was not located, stops the loop
            break
        if(stuck(Elapse_Time,c887)==True):
           return
        Can_Move_There=c887.ReadGCSCommand('vmo? u '+f"{Tilt_X}"+ ' v '+f"{Tilt_Y}") # Ask if the current position we are going to pass is acceptable
        if(int(Can_Move_There)==1): # if the next command is acceptable
            c887.GcsCommandset('MOV U '+f"{Tilt_X}"+' V '+f"{Tilt_Y}") #Sends the movement command to hexapod
            time.sleep(.02)# sleeps because the loop is too fast and see the ball twice at the same location messing up the movement
#*********************************************
'''
Input: Location of the Ball 
Output: The region of the ball, or a zero
Description: Takes the ball location and searches in the Region Dictionary to find a matching region
'''
def Region_Detection(Ball_Local):
    for reg in Region: #The for loop goes through the Dictionary for each region
        Curr_X=Ball_Local[0]-Origin_X #Current Ball Location in X
        Curr_Y=Ball_Local[1]-Origin_Y # Current Ball Location in Y
        Curr_Angle=-1*(((math.atan2(Curr_Y,Curr_X))*180/math.pi)) #Current Angle, mutiplying by -1 becasue Atan2 things I guess
        if(Curr_Angle<0): #If the angle is less than 0 than add 360 because Atan2 things I guess IDK
            Curr_Angle=Curr_Angle+360
        Curr_Radius=math.sqrt((Curr_X**2)+(Curr_Y**2)) # finds the hyptenuse from origin to location to get the current radius
        Region_IR=Region[reg]["Area"][0] #The region inner radius Min
        Region_OR=Region[reg]["Area"][1] #The region outer radius Max
        Region_MinA=Region[reg]["Area"][2] #The region minimum Angle
        Region_MaxA=Region[reg]["Area"][3] # The region maximum Angle
        if(Curr_Radius>=Region_IR and Curr_Radius<=Region_OR): #Checks to see if the ball falls within the regions radiuses
            if(Curr_Angle>=Region_MinA and Curr_Angle<=Region_MaxA): #Checks to see if the ball fals within the regions Angles
                return reg # if the ball location falls between the angles and radius, return region
    return 0 # if none of the regions satisfy it, return 0
#*********************************************
'''
Input: frame from camera, Ball tracking list 
Output: The position of the ball, or a zero
Description: Takes the current frame and returns a ball location  based on the find contours function
'''
def Ball_detection(frame,Ball_Tracking):
    #Note: the frame is already filtered on a seperate thread so the frame is just contours (99% of the time just 1)
    contours,_=cv2.findContours(frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # Uses the find contour to get a list of contours in the frame
    for cnt in contours: # goes through the list of conturs found
        areas=cv2.contourArea(cnt) # gets the area of the contour
        #Size of Marble contour is affected by several factors such as distance away from camera, lighting, and perspective, if any part of the apparatice
        #is changed, the area factor may need to be changed
        if (areas>1 and areas<40): # Checks to see if the contour size is betwewn 1-40 pixels (this range was tested for but may change based on variety of factors)
            x,y,w,h=cv2.boundingRect(cnt)# takes the contour and gives the (X,Y) coordinates of the upper corner, and the width and height of contour
            if len(Ball_Tracking)<10: #will only append the Ball location if the Ball tracking list is less than 10 locations
                Ball_Tracking.append((x,y))
            else: #If the amount of Balls is more than 10, remove the first element and put the newest location in
                Ball_Tracking.pop(0)
                Ball_Tracking.append((x,y))
            x=int(x+(w/2)) #Since the boundingRect Function gives you the corner location of the contour, use this equation to get the center of the contour/Marble
            y=int(y+(h/2)) #Since the boundingRect Function gives you the corner location of the contour, use this equation to get the center of the contour/Marble
            Ball_Current_Location=(x,y)
            return Ball_Current_Location #Returns the Center Location of the ball
    #Every thing below does the same appending to ball tracking list but if there is no contours that match the area, return 0 and add 0 to the Ball tracking list
    if len(Ball_Tracking)<10:
        Ball_Tracking.append((0,0))
    else:
        Ball_Tracking.pop(0)
        Ball_Tracking.append((0,0))
    return 0
#*********************************************
'''
Input: linear or rotary motion input, values, controller
Ouput: nothing
Definition: Depending on the movement, it willl command the Hexapod to move a certain way and query it untilll it gets to its destinaiton
'''
def ONT(T, values,c887):
    if(T=='UVW'):
        c887.GcsCommandset('MOV U ' +str(values[0])+ ' V '+str(values[1])+' W '+str(values[2]))
        Target=c887.ReadGCSCommand('ont?')
        Target_Sum=(int(Target[2])+int(Target[7])+int(Target[12])+int(Target[17])+int(Target[22])+int(Target[27]))
        while(Target_Sum!=6):
            c887.GcsCommandset('MOV U ' +str(values[0])+ ' V '+str(values[1])+' W '+str(values[2]))
            Target=c887.ReadGCSCommand('ont?')
            Target_Sum=(int(Target[2])+int(Target[7])+int(Target[12])+int(Target[17])+int(Target[22])+int(Target[27]))
            time.sleep(.01)
    else:
        c887.GcsCommandset('MOV X ' +str(values[0])+ ' Y '+str(values[1])+' Z '+str(values[2]))
        Target=c887.ReadGCSCommand('ont?')
        Target_Sum=(int(Target[2])+int(Target[7])+int(Target[12])+int(Target[17])+int(Target[22])+int(Target[27]))
        while(Target_Sum!=6):
            c887.GcsCommandset('MOV X ' +str(values[0])+ ' Y '+str(values[1])+' Z '+str(values[2]))
            Target=c887.ReadGCSCommand('ont?')
            Target_Sum=(int(Target[2])+int(Target[7])+int(Target[12])+int(Target[17])+int(Target[22])+int(Target[27]))
            time.sleep(.01)
'''
Input: Controller
Output: none
Definition: After a victory Royale (getting to the middle" the Hexapod will push the ball through the ramp and then rotate and go up and down
'''
def fortnite_emote(c887):
    time.sleep(1)
    c887.GcsCommandset('VLS 50')
    Vel=c887.ReadGCSCommand('vls?')
    while(int(Vel)!=50):
        c887.GcsCommandset('VLS 50')
        Vel=c887.ReadGCSCommand('vls?')
    ONT('UVW', [14,0,0],c887)
    ONT('UVW', [0,0,0],c887)
    ONT('XYZ', [0,0,0],c887)
    ONT('UVW', [0,0,-30],c887)
    ONT('UVW', [0,0,30],c887)
    ONT('UVW', [0,0,0],c887)
    ONT('XYZ', [0,0,24],c887)
    ONT('XYZ', [0,0,0],c887)
    c887.GcsCommandset('VLS 10')
    Vel=c887.ReadGCSCommand('vls?')
    while(int(Vel)!=10):
        c887.GcsCommandset('VLS 10')
        Vel=c887.ReadGCSCommand('vls?')