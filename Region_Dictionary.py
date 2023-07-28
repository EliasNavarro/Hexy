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

ring1_1=create_region((458,469),267,308,265,277)#298,310)
ring1_2=create_region((458, 469),275,308,181,268) #2 degree overlap
ring1_3=create_region((458, 469),269,308,87,184) #5 degree overlap
ring1_4=create_region((458, 469),269,308,-3,87)  #5 degree overlap
ring1_5=create_region((458, 469),275,308,-86,0)  #2 degree overlap
ramp=create_region((458,469),80,279,-7,4)

# ring2_1=create_region((308, 252),155,200,-25,26)
# ring2_2=create_region((308, 252),155,200,225,340)
# ring2_3=create_region((308, 252),155,200,202,230)
# ring2_4=create_region((308, 252),155,200,110,210)
# ring2_5=create_region((308, 252),155,200,40,110)

# ring3_1=create_region((308, 252),113,150,-40,23)
# ring3_2=create_region((308, 252),113,150,240,320)
# ring3_3=create_region((308, 252),113,150,140,245)
# ring3_4=create_region((308, 252),113,150,105,145)
# ring3_5=create_region((308, 252),113,150,43,110)

convert=math.pi/180

P=.0017
I=0#0.000009
D=.09
P_out=.001
I_out=0#0.000009
D_out=.01

P_2=0.0025
I_2=0.00001
D_2=0.09
Region = {
  "Ring1_1" :{"Area":ring1_1,"X_pos":0,
                             "Y_pos":-10,
                             "P Gain":0.0015,
                             "I Gain":0.00,
                             "D Gain":0.00,
                             "Target":[int(210*math.cos(271*convert)+458),int(210*math.sin(271*convert)+469)], #[x,y]
                              "Stuck":[[-3,0]]},
   "Ring1_2" :{"Area":ring1_2,"X_pos":1,
                              "Y_pos":5,#-1
                              "P Gain":P,#.003,
                               "I Gain":I,#0.00001,
                               "D Gain":D,#0.1,
                              "Target":[int(287*math.cos(271*convert)+458),int(287*math.sin(271*convert)+469)],
                              "Stuck":[[5,0]]},
  "Ring1_3" :{"Area":ring1_3,"X_pos":-5,
                             "Y_pos":5,
                             "P Gain":P_out,#.0015,
                             "I Gain":I_out,#0,
                             "D Gain":D_out,#0.1,
                             "Target":[int(287*math.cos(271*convert)+458),int(287*math.sin(271*convert)+469)],
                             "Stuck":[[0,5]]},
   "Ring1_5" :{"Area":ring1_5,"X_pos":-1,
                              "Y_pos":5,#1
                              "P Gain":P+.001,#.003,
                              "I Gain":I,#0.00001,
                              "D Gain":D-.02,#0.1,
                              "Target":[int(287*math.cos(271*convert)+458),int(287*math.sin(271*convert)+469)],
                              "Stuck":[[7,0]]},
   "Ring1_4" :{"Area":ring1_4,"X_pos":5,
                               "Y_pos":5,
                               "P Gain":P_out,#.0015,
                               "I Gain":I_out,#0,
                               "D Gain":D_out,#.1,
                               "Target":[int(287*math.cos(271*convert)+458),int(287*math.sin(271*convert)+469)],
                               "Stuck":[[0,5]]},
   "Ramp_0" :{"Area":ramp,"X_pos":2.5,
                               "Y_pos":10,
                               "P Gain":0,
                               "I Gain":0.0000,
                               "D Gain":0.00,
                               "Target":[int(300*math.cos(-1*convert)+458),int(300*math.sin(-1*convert)+469)],
                               "Stuck":[[-10,1]]},

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
