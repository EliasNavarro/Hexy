import numpy as np
import math
'''
Description: A Dictionary of all the Regions in the Maze with their region Area, HexaPod tilt in the X,Y direct,PID Values, and Specified target
Note: Ramp is divided into two parts since its angle lies between 0-4 degrees and 356-360 degrees
'''
Origin_X=53 #Origin of the X Axis which is located in th center of the Maze
Origin_Y=46 #Origin of the Y Axis which is located in th center of the Maze

convert=math.pi/180 # Conversion from degrees to radians
#PID Values for the two regions around the target region of the first ring
P_1=.011
I_1=0.09
D_1=1.05
#PID Values for the two regions farthest from the first ring target
P_out=.0008
I_out=0.1
D_out=0.05
#PID Values for the 2nd ring
P_2=0.01
I_2=0.07
D_2=.9
#PID Values for the 3rd ring
P_3=0.01
I_3=0.08
D_3=.95
#PID Values for the 4th ring
P_4=0.01
I_4=0.1
D_4=.95
#Note: The entrance regions and ramps have targets and PIDS but are not used because in the code, those special Regions just go straight to their target position jsut to knock the ball in quickly
Region = {
  "Ring1_1" :{"Area":[38,47,82,97],#[Inner Diameter, Outer Diameter, Min Angle, Max Angle]
                              "X_pos":-1,#Hexapod X tilt
                             "Y_pos":-5,#Hexapod Y tilt
                             "P Gain":0.01,#P Value in PID
                             "I Gain":0.00,# I Value in PID
                             "D Gain":0.00,# D Value in PID
                             "Target":[int(30*math.cos(-89*convert)+Origin_X),int(30*math.sin(-89*convert)+Origin_Y)]},# Taget position of the ball
                            #Note:Each ring has the same target except for the entrance regions (which as stated above aren't used)
  "Ring1_2" :{"Area":[40,47,94,195],"X_pos":.5,
                              "Y_pos":4,
                              "P Gain":P_1,
                               "I Gain":I_1,
                               "D Gain":D_1,
                              "Target":[int(47*math.cos(-89*convert)+Origin_X),int(47*math.sin(-89*convert)+Origin_Y)]},
  "Ring1_3" :{"Area":[40,47,193,270],"X_pos":-5,
                             "Y_pos":2,
                             "P Gain":P_out,
                             "I Gain":I_out,
                             "D Gain":D_out,
                             "Target":[int(47*math.cos(-89*convert)+Origin_X),int(47*math.sin(-89*convert)+Origin_Y)]},
   "Ring1_5" :{"Area":[41,47,0,84],"X_pos":-.5,
                              "Y_pos":4,
                              "P Gain":P_1,
                              "I Gain":I_1,
                              "D Gain":D_1,
                              "Target":[int(47*math.cos(-89*convert)+Origin_X),int(47*math.sin(-89*convert)+Origin_Y)]},
   "Ring1_4" :{"Area":[40,47,270,360],"X_pos":4,
                               "Y_pos":2,
                               "P Gain":P_out,
                               "I Gain":I_out,
                               "D Gain":D_out,
                               "Target":[int(47*math.cos(-89*convert)+Origin_X),int(47*math.sin(-89*convert)+Origin_Y)]},
   "Ramp0_1" :{"Area":[10,40,0,4],"X_pos":14,
                               "Y_pos":1,
                               "P Gain":0,
                               "I Gain":1,
                               "D Gain":0.0,
                               "Target":[int(47*math.cos(0*convert)+Origin_X),int(47*math.sin(0*convert)+Origin_Y)]},
   "Ramp0_2" :{"Area":[10,40,356,360],"X_pos":14,
                               "Y_pos":1,
                               "P Gain":0,
                               "I Gain":1,
                               "D Gain":0.00,
                               "Target":[int(47*math.cos(0*convert)+Origin_X),int(47*math.sin(0*convert)+Origin_Y)]},
    "Ring2_1" :{"Area":[30,38,6,80],"X_pos":-4,
                                 "Y_pos":1,
                                 "P Gain":P_2,
                                 "I Gain":I_2,
                                 "D Gain":D_2,
                                 "Target":[int(38*math.cos(-178*convert)+Origin_X),int(38*math.sin(-178*convert)+Origin_Y)]},
     "Ring2_3" :{"Area":[29,39,167,190],"X_pos":5,
                                 "Y_pos":-1,
                                "P Gain":.1,
                                 "I Gain":0.1,
                                 "D Gain":0,
                                 "Target":[int(22*math.cos(-178*convert)+Origin_X),int(22*math.sin(-178*convert)+Origin_Y)]},
       "Ring2_2" :{"Area":[30,39,80,169],"X_pos":-5,
                                 "Y_pos":-.2,
                                 "P Gain":P_2,
                                  "I Gain":I_2,
                                  "D Gain":D_2,
                                 "Target":[int(38*math.cos(-178*convert)+Origin_X),int(38*math.sin(-178*convert)+Origin_Y)]},
       "Ring2_4" :{"Area":[31,39,189,300],"X_pos":-5,
                                   "Y_pos":.2,
                                   "P Gain":P_2,
                                   "I Gain":I_2,
                                   "D Gain":D_2,
                                   "Target":[int(38*math.cos(-178*convert)+Origin_X),int(38*math.sin(-178*convert)+Origin_Y)]},
       "Ring2_5" :{"Area":[31,39,300,353],"X_pos":-5,
                                   "Y_pos":-3,
                                   "P Gain":P_2,
                                   "I Gain":I_2,
                                   "D Gain":D_2,
                                   "Target":[int(38*math.cos(-178*convert)+Origin_X),int(38*math.sin(-178*convert)+Origin_Y)]},
      "Ring3_4" :{"Area":[21,29,259,288],"X_pos":0,
                                   "Y_pos":5,
                                   "P Gain":.2,
                                   "I Gain":0.1,
                                  "D Gain":0,
                                   "Target":[int(12*math.cos(-273*convert)+Origin_X),int(12*math.sin(-273*convert)+Origin_Y)]},
      "Ring3_3" :{"Area":[21,29,166,260],"X_pos":.1,
                                   "Y_pos":-5,
                                   "P Gain":P_3,
                                   "I Gain":I_3,
                                   "D Gain":D_3,
                                   "Target":[int(29*math.cos(-273*convert)+Origin_X),int(29*math.sin(-273*convert)+Origin_Y)]},
       "Ring3_2" :{"Area":[21,29,80,166],"X_pos":-5,
                                   "Y_pos":-.5,
                                   "P Gain":P_3,
                                   "I Gain":I_3,
                                   "D Gain":D_3,
                                   "Target":[int(29*math.cos(-273*convert)+Origin_X),int(29*math.sin(-273*convert)+Origin_Y)]},
     "Ring3_1" :{"Area":[21,29,6,80],"X_pos":-1,
                                 "Y_pos":5,
                                 "P Gain":P_3,
                                 "I Gain":I_3,
                                 "D Gain":D_3,
                                 "Target":[int(29*math.cos(-273*convert)+Origin_X),int(29*math.sin(-273*convert)+Origin_Y)]},
      "Ring3_5" :{"Area":[21,29,288,349],"X_pos":-.1,
                                 "Y_pos":-5,
                                 "P Gain":P_3,
                                 "I Gain":I_3,
                                 "D Gain":D_3,
                                 "Target":[int(29*math.cos(-273*convert)+Origin_X),int(29*math.sin(-273*convert)+Origin_Y)]},
        "Ring4_4" :{"Area":[12,20,70,110],"X_pos":0,
                                   "Y_pos":-10,
                                   "P Gain":.3,
                                   "I Gain":0.2,
                                  "D Gain":0,
                                   "Target":[int(0*math.cos(-90*convert)+Origin_X),int(0*math.sin(-90*convert)+Origin_Y)]},
      "Ring4_3" :{"Area":[14,20,110,200],"X_pos":1,
                                   "Y_pos":5,
                                   "P Gain":P_4,
                                   "I Gain":I_4,
                                   "D Gain":D_4,
                                   "Target":[int(20*math.cos(-90*convert)+Origin_X),int(20*math.sin(-90*convert)+Origin_Y)]},
       "Ring4_2" :{"Area":[14,21,200,294],"X_pos":-5,
                                   "Y_pos":1,
                                   "P Gain":P_4,
                                   "I Gain":I_4,
                                   "D Gain":D_4,
                                   "Target":[int(20*math.cos(-90*convert)+Origin_X),int(20*math.sin(-90*convert)+Origin_Y)]},
     "Ring4_1" :{"Area":[14,21,294,348],"X_pos":-5,
                                 "Y_pos":-.5,
                                 "P Gain":P_4,
                                 "I Gain":I_4,
                                 "D Gain":D_4,
                                 "Target":[int(20*math.cos(-90*convert)+Origin_X),int(20*math.sin(-90*convert)+Origin_Y)]},
      "Ring4_5" :{"Area":[13,20,18,70],"X_pos":-1,
                                 "Y_pos":5,
                                 "P Gain":P_4,
                                 "I Gain":I_4,
                                 "D Gain":D_4,
                                 "Target":[int(20*math.cos(-90*convert)+Origin_X),int(20*math.sin(-90*convert)+Origin_Y)]},
      "Ring5_1" :{"Area":[0,12,0,360],"X_pos":14,
                                 "Y_pos":0,
                                 "P Gain":0,
                                 "I Gain":1,
                                 "D Gain":0,
                                 "Target":[int(47*math.cos(0*convert)+Origin_X),int(47*math.sin(0*convert)+Origin_Y)]},
 
}
