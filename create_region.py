
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
