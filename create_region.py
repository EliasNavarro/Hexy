# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:55:08 2023

@author: maena
"""
import math
def create_region(center,inner_ring,outer_ring,start,end):
    ring_girth=outer_ring-inner_ring
    region=[]
    convert=math.pi/180
    for i in range(ring_girth):
        for j in range(start,end):
            x=int((inner_ring+i)*math.cos((-j)*convert)+center[0])
            y=int((inner_ring+i)*math.sin((-j)*convert)+center[1])
            region.append((x,y))
    return region
