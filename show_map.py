import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
from Region_Dictionary import Region, Origin_X, Origin_Y
import math
from Camera import VideoGet
import cv2
convert=math.pi/180

"""
Input: Center of maze (X,Y), inner_ring radius, outer_ring radius, start angle, end anlge
Output: A list of points of the region
Description: Takes region parameters and creat a list of all the possibles area in the region
Note: Not used in the actual code, just to create graph of ring in show_map
"""
import math
def create_region(center,inner_ring,outer_ring,start,end):
    ring_girth=outer_ring-inner_ring 
    region=[]
    convert=math.pi/180
    for i in range(ring_girth):
        for j in range(start,end):
            x=int((inner_ring+i)*math.cos(-(j)*convert)+center[0])
            y=int((inner_ring+i)*math.sin(-(j)*convert)+center[1])
            region.append((x,y))
    return region

'''
Input: A frame from the PiCam
Output: Two plots of the Maze
Description: Looks in the Region Dictionary and plots the regions and creates another region that graphs the target postions of the regions
'''
def show_map(frame):
    fig, ax = plt.subplots()
    ax.imshow(frame)
    plt.title("Regions")
    for i in Region: #A "for loop" that goes through the whole Dictionary 
        Inner_D=Region[i]["Area"][0] #Inner Diamter of region
        Outer_D=Region[i]["Area"][1] #Outer Diameter of region
        A_Min=Region[i]["Area"][2] # Minimum Angle of the region
        A_Max=Region[i]["Area"][3] #Maximum Angle of the region
        ring=create_region((Origin_X,Origin_Y),Inner_D,Outer_D,A_Min,A_Max) # a Custom Function that creats multiple points in the rgion
        plt.scatter([item[0] for item in ring], [item[1] for item in ring], s=1) # Plots the regions in a scatter plot 
 
    fig, ax = plt.subplots()
    ax.imshow(frame)
    plt.title("Targets/ Goals")
    plt.scatter(int(47*math.cos(-89*convert)+Origin_X),int(47*math.sin(-89*convert)+Origin_Y),s=15) #Target Positions  of all the regions
    plt.scatter(int(30*math.cos(-89*convert)+Origin_X),int(30*math.sin(-89*convert)+Origin_Y),s=15)
    plt.scatter(int(47*math.cos(0*convert)+Origin_X),int(47*math.sin(0*convert)+Origin_Y),s=15)
    plt.scatter(int(38*math.cos(-178*convert)+Origin_X),int(38*math.sin(-178*convert)+Origin_Y),s=15)
    plt.scatter(int(22*math.cos(-178*convert)+Origin_X),int(22*math.sin(-178*convert)+Origin_Y),s=15)
    plt.scatter(int(29*math.cos(-273*convert)+Origin_X),int(29*math.sin(-273*convert)+Origin_Y),s=15)
    plt.scatter(int(12*math.cos(-273*convert)+Origin_X),int(12*math.sin(-273*convert)+Origin_Y),s=15)
    plt.scatter(int(20*math.cos(-90*convert)+Origin_X),int(20*math.sin(-90*convert)+Origin_Y),s=15)
    plt.scatter(int(0*math.cos(-90*convert)+Origin_X),int(0*math.sin(-90*convert)+Origin_Y),s=15)
    plt.show()
'''
Input: Raw Frame
Output: Filtered Frame
Description: Crops and Blurs frame to get a viewable picture of the frame, only used in debugging
'''
def threadVideoGet(source):
    video_getter = VideoGet().start() #Initates and starts Camera collecting
    while True:
        frame_Cam = video_getter.frame # Collects frame of what the camera sees
        frame_OG=video_getter.preserved_frame# collects frame non filtered
#         width=int(frame.shape[1]*3) # increases frame size for easier looking
#         height=int(frame.shape[0]*3)  increases frame size for easier looking
        cv2.imshow("Filter Image", frame_Cam) # show image
        cv2.imshow("Unfiltered Image", frame_OG) # show image
        if (cv2.waitKey(1) == ord("q")) or video_getter.stopped: # if the q key is pressed stop video
            video_getter.stop()
            cv2.destroyAllWindows()
            break
    show_map(frame_OG) # show plot of regions of the video
threadVideoGet(0) #just starts the code 
