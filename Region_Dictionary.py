# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 10:08:18 2023

@author: maena
"""
from create_region import create_region
import numpy as np
import math

def create_list(ranges,steps):
    lists=[]
    for i in range(len(ranges)-1):
       lists=np.concatenate((lists,np.linspace(ranges[i],ranges[i+1], num=steps))) 
    return lists
Origin_X=50
Origin_Y=50

convert=math.pi/180

PL=.012
IL=0.1#0.000009
DL=.95
PR=.012
IR=0.1#0.000009
DR=.95
P_out=.0008
I_out=0.1#0.000009
D_out=0.04#.01

P_2=0.003
I_2=0.00001
D_2=0.09
Region = {
  "Ring1_1" :{"Area":[38,47,82,97],#[Inner Diameter, Outer Diameter, Min Angle, Max Angle]
                              "X_pos":0,
                             "Y_pos":-5,#-10,
                             "P Gain":0.01,
                             "I Gain":0.00,
                             "D Gain":0.00,
                             "Target":[int(30*math.cos(-89*convert)+50),int(30*math.sin(-89*convert)+50)], #[x,y]
                              "Stuck":[[-3,0]]},
   "Ring1_2" :{"Area":[40,47,94,195],"X_pos":.5,
                              "Y_pos":4,
                              "P Gain":PL,#.003,
                               "I Gain":IL,#0.00001,
                               "D Gain":DL,#0.1,
                              "Target":[int(47*math.cos(-89*convert)+50),int(47*math.sin(-89*convert)+50)],
                              "Stuck":[[5,0]]},
  "Ring1_3" :{"Area":[40,47,193,270],"X_pos":-5,
                             "Y_pos":2,
                             "P Gain":P_out,#.0015,
                             "I Gain":I_out,#0,
                             "D Gain":D_out,#0.1,
                             "Target":[int(89*math.cos(-88*convert)+97),int(89*math.sin(-88*convert)+89)],
                             "Stuck":[[0,5]]},
   "Ring1_5" :{"Area":[41,47,0,84],"X_pos":-.5,
                              "Y_pos":4,#1
                              "P Gain":PR,#.003,
                              "I Gain":IR,#0.00001,
                              "D Gain":DR,
                              "Target":[int(47*math.cos(-89*convert)+50),int(47*math.sin(-89*convert)+50)],
                              "Stuck":[[7,0]]},
   "Ring1_4" :{"Area":[40,47,270,360],"X_pos":4,
                               "Y_pos":2,
                               "P Gain":P_out,#.0015,
                               "I Gain":I_out,#0,
                               "D Gain":D_out,#.1,
                               "Target":[int(89*math.cos(-88*convert)+97),int(89*math.sin(-88*convert)+89)],
                               "Stuck":[[0,5]]},
#    "Ramp_0" :{"Area":ramp,"X_pos":10,
#                                "Y_pos":0,
#                                "P Gain":0.01,
#                                "I Gain":0.0000,
#                                "D Gain":0.00,
#                                "Target":[int(300*math.cos(-1*convert)+458),int(300*math.sin(-1*convert)+469)],
#                                "Stuck":[[-10,1]]},

    # "Ring2_1" :{"Area":ring2_1,"X_pos":5,
    #                             "Y_pos":0,
    #                             "P Gain":P_2,#.01,
    #                             "I Gain":I_2,#0.0000,
    #                             "D Gain":D_2,
    #                             "Target":[int(175*math.cos(219*convert)+308),int(175*math.sin(219*convert)+252)], #[x,y]
    #                             "Stuck":[[5,0]]},
    # "Ring2_3" :{"Area":ring2_3,"X_pos":0,
    #                             "Y_pos":-10,
    #                             "P Gain":P_2,#0.015,
    #                             "I Gain":I_2,#0.0000,
    #                             "D Gain":D_2,
    #                             "Target":[int(135*math.cos(219*convert)+308),int(135*math.sin(219*convert)+252)],
    #                             "Stuck":[[0,-10]]},
    #   "Ring2_2" :{"Area":ring2_2,"X_pos":-1,
    #                             "Y_pos":4,
    #                             "P Gain":P_2,#.007,
    #                              "I Gain":I_2,#0.0000,
    #                              "D Gain":D_2,
    #                             "Target":[int(175*math.cos(219*convert)+308),int(175*math.sin(219*convert)+252)],
    #                             "Stuck":[[0,5]]},

    #   "Ring2_4" :{"Area":ring2_4,"X_pos":1,
    #                               "Y_pos":4,
    #                               "P Gain":P_2,#.0015,
    #                               "I Gain":I_2,#0.0000,
    #                               "D Gain":D_2,
    #                               "Target":[int(175*math.cos(219*convert)+308),int(175*math.sin(219*convert)+252)],
    #                               "Stuck":[[0,5]]},
    #   "Ring2_5" :{"Area":ring2_5,"X_pos":-5,
    #                               "Y_pos":1,
    #                               "P Gain":P_2,#.0015,
    #                               "I Gain":I_2,#0.0000,
    #                               "D Gain":D_2,
    #                               "Target":[int(175*math.cos(219*convert)+308),int(175*math.sin(219*convert)+252)],
    #                               "Stuck":[[-5,0]]},
      
    #   "Ring3_3" :{"Area":ring3_3,"X_pos":10,
    #                               "Y_pos":0,
    #                               "P Gain":0.015,
    #                               "I Gain":0.0000,
    #                               "Target":[int(85*math.cos(125*convert)+308),int(85*math.sin(125*convert)+252)],
    #                               "Stuck":[[0,10],[0,-10]]},
    #   "Ring3_2" :{"Area":ring3_2,"X_pos":-5,
    #                               "Y_pos":0,
    #                               "P Gain":.003,
    #                               "I Gain":0.0000,
    #                               "Target":[int(133*math.cos(140*convert)+308),int(133*math.sin(140*convert)+252)],
    #                               "Stuck":[[-10,0]]},

    # "Ring3_1" :{"Area":ring3_1,"X_pos":0,
    #                             "Y_pos":5,
    #                             "P Gain":.007,
    #                             "I Gain":0.0000,
    #                             "Target":[int(133*math.cos(-135*convert)+308),int(133*math.sin(-135*convert)+252)], #[x,y]
    #                             "Stuck":[[10,0]]},
 
      # "Ring3_4" :{"Area":ring3_4,"X_pos":-8,
      #                             "Y_pos":0,
      #                             "P Gain":.003,
      #                             "I Gain":0.0000,
      #                             "Target":[int(133*math.cos(112*convert)+308),int(133*math.sin(112*convert)+252)],
      #                               "Stuck":[[-5,-5],[-5,5]]},

}
