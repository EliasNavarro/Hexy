import cv2
from Region_Dictionary import Region
from Region_Detection import Region_Detection,Ball_detection,Move_Hexxy_JR
from picamera2 import Picamera2
from Camera import VideoGet
from PIJoystick import PIJoystick
from pipython.pidevice.gcsmessages import GCSMessages
from pipython.pidevice.gcscommands import GCSCommands
from pipython.pidevice.interfaces.piserial import PISerial
'''
Input: Joystick class, controller
Output: Nothing
Description: Main FUnction that takes collects ball location and moves the hexapod based off it
'''
def Auto_Solver(joystick,c887):
    c887.GcsCommandset('MOV U 0 V 0 W 0') #Zero the HexaPod in UVW
    c887.GcsCommandset('MOV X 0 Y 0 Z 0') #Zero Hexapod in XYZ
    c887.GcsCommandset('VLS 10') #Sets Hexapod Velocity to 10
    video_getter= VideoGet() # Initates Picamera class to  collect vido on a seperate thread
    video_getter.start() # starts the thread
    Ball_Tracking=[(0,0)] # List of where the balls been, have a filler value to begin
    Prev_Region="Deez Nuts" # Variable of Previus Region used in other function, has a filler value to begin
    Error_List=[0,0] #List of the Error of the Ball from target, has two filler variables to begin with
    while (joystick.read()[2]==0): # Reads Joystick, continues to autosolve untill left button is pressed
        frame = video_getter.frame # Takes frame from camera
        P_frame=video_getter.preserved_frame # Takes preserved Frame (not used only in debugging)
        Ball_Location=Ball_detection(frame,Ball_Tracking) # Uses Ball_Detection to get the coordinates of the ball, if none its 0
        if(Ball_Location!=0): # Checks to see if there is a ball detected
            Current_Region=Region_Detection(Ball_Location) #Uses Region Detection to check if there is a region associated with ball location, if not its 0
            if(Current_Region!=0):# if there is an associated region
                if(Current_Region[4]!=Prev_Region[4]): #if the current region ring (thats why its the 5th element of ex. "Ring5_5" and "Ring4_5") is different than before ( last check region) reset the Ball tracking and error list
                    Ball_Tracking=[(0,0)] # reset Ball tracking
                    Error_List=[0,0] # reset error tracking
                #print(Current_Region)
                Move_Hexxy_JR(Current_Region,Ball_Tracking,Error_List,video_getter,joystick,c887) # based on all the information, sends it to Move _Hexy_JR to move the Hexapod
                Prev_Region=Current_Region # sets currents region to previus region
    video_getter.stop()#Stops Video Collection
    c887.GcsCommandset('MOV U 0 V 0 W 0')# set the hexapod to 0
    return
# 
# joy = PIJoystick()
# gateway = PISerial("/dev/ttyUSB0", 115200)
# messages = GCSMessages(gateway)
# c887 = GCSCommands(gcsmessage=messages)
# while(1):
#     Auto_Solver(joy,c887)
#     print("doodoo")
#     break
