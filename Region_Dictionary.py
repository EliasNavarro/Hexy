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
Origin_X=53
Origin_Y=46

convert=math.pi/180

PL=.012
IL=0.13#0.000009
DL=1.0
PR=.012
IR=0.13#0.000009
DR=1.0
P_out=.0008
I_out=0.1#0.000009
D_out=0.04#.01

P_2=0.01
I_2=0.1
D_2=.95
P_3=0.01
I_3=0.1
D_3=.95
P_4=0.01
I_4=0.1
D_4=.95
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
                             "Target":[int(47*math.cos(-89*convert)+50),int(47*math.sin(-89*convert)+50)],
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
                               "Target":[int(47*math.cos(-89*convert)+50),int(47*math.sin(-89*convert)+50)],
                               "Stuck":[[0,5]]},
   "Ramp0_1" :{"Area":[10,40,0,4],"X_pos":14,
                               "Y_pos":1,
                               "P Gain":0,
                               "I Gain":1,
                               "D Gain":0.0,
                               "Target":[int(47*math.cos(0*convert)+50),int(47*math.sin(0*convert)+50)],
                               "Stuck":[[-10,1]]},
   "Ramp0_2" :{"Area":[10,40,356,360],"X_pos":14,
                               "Y_pos":1,
                               "P Gain":0,
                               "I Gain":1,
                               "D Gain":0.00,
                               "Target":[int(47*math.cos(0*convert)+50),int(47*math.sin(0*convert)+50)],
                               "Stuck":[[-10,1]]},

    "Ring2_1" :{"Area":[30,38,6,80],"X_pos":-5,
                                 "Y_pos":2,
                                 "P Gain":P_2,#.01,
                                 "I Gain":I_2,#0.0000,
                                 "D Gain":D_2,
                                 "Target":[int(38*math.cos(-178*convert)+50),int(38*math.sin(-178*convert)+50)], #[x,y]
                                 "Stuck":[[5,0]]},
     "Ring2_3" :{"Area":[29,39,167,190],"X_pos":5,
                                 "Y_pos":0,
                                "P Gain":.1,#0.015,
                                 "I Gain":0.1,#0.0000,
                                 "D Gain":0,
                                 "Target":[int(22*math.cos(-178*convert)+50),int(22*math.sin(-178*convert)+50)],
                                 "Stuck":[[0,-10]]},
       "Ring2_2" :{"Area":[30,39,80,169],"X_pos":-5,
                                 "Y_pos":-.5,
                                 "P Gain":P_2,#.007,
                                  "I Gain":I_2,#0.0000,
                                  "D Gain":D_2,
                                 "Target":[int(38*math.cos(-178*convert)+50),int(38*math.sin(-178*convert)+50)],
                                 "Stuck":[[0,5]]},

       "Ring2_4" :{"Area":[31,39,189,300],"X_pos":-5,
                                   "Y_pos":.5,
                                   "P Gain":P_2,#.0015,
                                   "I Gain":I_2,#0.0000,
                                   "D Gain":D_2,
                                   "Target":[int(38*math.cos(-178*convert)+50),int(38*math.sin(-178*convert)+50)],
                                   "Stuck":[[0,5]]},
       "Ring2_5" :{"Area":[31,39,300,353],"X_pos":-5,
                                   "Y_pos":-3,
                                   "P Gain":P_2,#.0015,
                                   "I Gain":I_2,#0.0000,
                                   "D Gain":D_2,
                                   "Target":[int(38*math.cos(-178*convert)+50),int(38*math.sin(-178*convert)+50)],
                                   "Stuck":[[-5,0]]},
      "Ring3_4" :{"Area":[21,29,259,288],"X_pos":0,
                                   "Y_pos":5,
                                   "P Gain":.2,
                                   "I Gain":0.1,
                                  "D Gain":0,
                                   "Target":[int(12*math.cos(-273*convert)+50),int(12*math.sin(-273*convert)+50)],
                                   "Stuck":[[-5,-5],[-5,5]]},
      "Ring3_3" :{"Area":[21,29,166,260],"X_pos":1,
                                   "Y_pos":-5,
                                   "P Gain":P_3,
                                   "I Gain":I_3,
                                   "D Gain":D_3,
                                   "Target":[int(29*math.cos(-273*convert)+50),int(29*math.sin(-273*convert)+50)],
                                   "Stuck":[[0,10],[0,-10]]},
       "Ring3_2" :{"Area":[21,29,80,166],"X_pos":-5,
                                   "Y_pos":-1,
                                   "P Gain":P_3,
                                   "I Gain":I_3,
                                   "D Gain":D_3,
                                   "Target":[int(29*math.cos(-273*convert)+50),int(29*math.sin(-273*convert)+50)],
                                   "Stuck":[[-10,0]]},

     "Ring3_1" :{"Area":[21,29,6,80],"X_pos":-1,
                                 "Y_pos":5,
                                 "P Gain":P_3,
                                 "I Gain":I_3,
                                 "D Gain":D_3,
                                 "Target":[int(29*math.cos(-273*convert)+50),int(29*math.sin(-273*convert)+50)], #[x,y]
                                 "Stuck":[[10,0]]},
      "Ring3_5" :{"Area":[21,29,288,349],"X_pos":-1,
                                 "Y_pos":-5,
                                 "P Gain":P_3,
                                 "I Gain":I_3,
                                 "D Gain":D_3,
                                 "Target":[int(29*math.cos(-273*convert)+50),int(29*math.sin(-273*convert)+50)], #[x,y]
                                 "Stuck":[[10,0]]},
        "Ring4_4" :{"Area":[12,20,70,110],"X_pos":0,
                                   "Y_pos":-10,
                                   "P Gain":.3,
                                   "I Gain":0.2,
                                  "D Gain":0,
                                   "Target":[int(0*math.cos(-90*convert)+50),int(0*math.sin(-90*convert)+50)],
                                   "Stuck":[[-5,-5],[-5,5]]},
      "Ring4_3" :{"Area":[14,20,110,200],"X_pos":1,
                                   "Y_pos":5,
                                   "P Gain":P_4,
                                   "I Gain":I_4,
                                   "D Gain":D_4,
                                   "Target":[int(20*math.cos(-90*convert)+50),int(20*math.sin(-90*convert)+50)],
                                   "Stuck":[[0,10],[0,-10]]},
       "Ring4_2" :{"Area":[14,21,200,294],"X_pos":-1,
                                   "Y_pos":5,
                                   "P Gain":P_4,
                                   "I Gain":I_4,
                                   "D Gain":D_4,
                                   "Target":[int(20*math.cos(-90*convert)+50),int(20*math.sin(-90*convert)+50)],
                                   "Stuck":[[-10,0]]},

     "Ring4_1" :{"Area":[14,21,294,348],"X_pos":-5,
                                 "Y_pos":-1,
                                 "P Gain":P_4,
                                 "I Gain":I_4,
                                 "D Gain":D_4,
                                 "Target":[int(20*math.cos(-90*convert)+50),int(20*math.sin(-90*convert)+50)], #[x,y]
                                 "Stuck":[[10,0]]},
      "Ring4_5" :{"Area":[13,20,18,70],"X_pos":-1,
                                 "Y_pos":5,
                                 "P Gain":P_4,
                                 "I Gain":I_4,
                                 "D Gain":D_4,
                                 "Target":[int(20*math.cos(-90*convert)+50),int(20*math.sin(-90*convert)+50)], #[x,y]
                                 "Stuck":[[10,0]]},
      "Ring5_1" :{"Area":[0,12,0,360],"X_pos":14,
                                 "Y_pos":0,
                                 "P Gain":0,
                                 "I Gain":1,
                                 "D Gain":0,
                                 "Target":[int(47*math.cos(0*convert)+50),int(47*math.sin(0*convert)+50)], #[x,y]
                                 "Stuck":[[10,0]]},
 


}
