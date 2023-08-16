import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
from create_region import create_region
from Region_Dictionary import Region, Origin_X, Origin_Y
import math
convert=math.pi/180
'''
Input: A frame from the PiCam
Output: Two plots of the Maze
Description: Looks in the Region Dictionary and plots the regions and creates another region that graphs the target postions of the regions
'''
def show_map(frame):
    fig, ax = plt.subplots()
    ax.imshow(frame)
    for i in Region: #A "for loop" that goes through the whole Dictionary 
        Inner_D=Region[i]["Area"][0] #Inner Diamter of region
        Outer_D=Region[i]["Area"][1] #Outer Diameter of region
        A_Min=Region[i]["Area"][2] # Minimum Angle of the region
        A_Max=Region[i]["Area"][3] #Maximum Angle of the region
        ring=create_region((Origin_X,Origin_Y),Inner_D,Outer_D,A_Min,A_Max) # a Custom Function that creats multiple points in the rgion
        plt.scatter([item[0] for item in ring], [item[1] for item in ring], s=1) # Plots the regions in a scatter plot 
 
    fig, ax = plt.subplots()
    ax.imshow(frame)
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
    
