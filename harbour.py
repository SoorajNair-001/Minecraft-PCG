from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL

import random
STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()

WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)
import numpy as np
import matplotlib as mpld
from matplotlib import pyplot

harbourPoints = []
def buildHarbor(locationGrid):
    print("Building harbours..")
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    X = STARTX + (ENDX - STARTX) // 2
    Z = STARTZ + (ENDZ - STARTZ) // 2

    # finding the water bodies in the area
    watergrid = np.zeros((len(heights),len(heights[0])))
    for i in range(0,len(watergrid)):
        for j in range(0,len(watergrid[0])):
            if INTF.getBlock(STARTX+i,heights[i][j]-1,STARTZ+j) =="minecraft:water":
                watergrid[i][j] = 1

    watergrid2 = watergrid.copy()
    # finding the edges of the water body
    for i in range(0,len(watergrid)):
        for j in range(0,len(watergrid[0])):
            if i-1>=0 and i+1<len(watergrid) and j-1>=0 and j+1<len(watergrid):
                if watergrid[i][j] == 1:
                    if not(watergrid[i-1][j] == 1 and watergrid[i+1][j] == 1 
                        and watergrid[i][j-1] == 1 and watergrid[i][j+1] == 1):
                        watergrid2[i][j] = 2
    for i in range(0,len(watergrid)):
        for j in range(0,len(watergrid[0])):
            if watergrid2[i][j] == 2:
                harbourPoints.append([i,j])

    # choosing three random spots
    randPoint = random.randint(0,len(harbourPoints)-1)
    while True:
        if (harbourPoints[randPoint][0]>5 and harbourPoints[randPoint][1]<len(heights[0])-5 ):
            collide = False
            for i in range(0,len(locationGrid)):
                for j in range(0,len(locationGrid[0])):
                    if locationGrid[i][j] == 1:
                        if (harbourPoints[randPoint][0]>i-10 and harbourPoints[randPoint][0]<i+10 
                            and harbourPoints[randPoint][1]>j-10 and harbourPoints[randPoint][1]<j+10):
                            collide = True

            if not collide:
                y1 = heights[(harbourPoints[randPoint][0],harbourPoints[randPoint][1])]
                placeHarbour(STARTX+harbourPoints[randPoint][0],y1,STARTZ+harbourPoints[randPoint][1])
                break
            else:
                randPoint = random.randint(0,len(harbourPoints)-1)  
        else:
            randPoint = random.randint(0,len(harbourPoints)-1)
    
    randPoint = random.randint(0,len(harbourPoints)-1)
    while True:
        if (harbourPoints[randPoint][0]>5 and harbourPoints[randPoint][1]<len(heights[0])-5 ):
            collide = False
            for i in range(0,len(locationGrid)):
                for j in range(0,len(locationGrid[0])):
                    if locationGrid[i][j] == 1:
                        if (harbourPoints[randPoint][0]>i-10 and harbourPoints[randPoint][0]<i+10 
                            and harbourPoints[randPoint][1]>j-10 and harbourPoints[randPoint][1]<j+10):
                            collide = True

            if not collide:
                y1 = heights[(harbourPoints[randPoint][0],harbourPoints[randPoint][1])]
                placeHarbour(STARTX+harbourPoints[randPoint][0],y1,STARTZ+harbourPoints[randPoint][1])
                break
            else:
                randPoint = random.randint(0,len(harbourPoints)-1)  
        else:
            randPoint = random.randint(0,len(harbourPoints)-1)
    
    randPoint = random.randint(0,len(harbourPoints)-1)
    while True:
        if (harbourPoints[randPoint][0]>5 and harbourPoints[randPoint][1]<len(heights[0])-5 ):
            collide = False
            for i in range(0,len(locationGrid)):
                for j in range(0,len(locationGrid[0])):
                    if locationGrid[i][j] == 1:
                        if (harbourPoints[randPoint][0]>i-10 and harbourPoints[randPoint][0]<i+10 
                            and harbourPoints[randPoint][1]>j-10 and harbourPoints[randPoint][1]<j+10):
                            collide = True

            if not collide:
                y1 = heights[(harbourPoints[randPoint][0],harbourPoints[randPoint][1])]
                placeHarbour(STARTX+harbourPoints[randPoint][0],y1,STARTZ+harbourPoints[randPoint][1])
                break
            else:
                randPoint = random.randint(0,len(harbourPoints)-1)  
        else:
            randPoint = random.randint(0,len(harbourPoints)-1)

# place harbour
def placeHarbour(x,y,z):
    size = 15
    X = x-(size//2)
    Z = z-(size//2)
    
    dir = []
    if INTF.getBlock(x+4,y-1,z) == "minecraft:water": dir.append([x+4,z])
    if INTF.getBlock(x-5,y-1,z) == "minecraft:water": dir.append([x-5,z])
    if INTF.getBlock(x,y-1,z+4) == "minecraft:water": dir.append([x,z+4])
    if INTF.getBlock(x,y-1,z-5) == "minecraft:water": dir.append([x,z-5])

    if len(dir)>0:
        for i in range(-4,4):
            for j in range(-4,4):
                for yy in range(0,5):
                    INTF.placeBlock(x+i,y-1+yy,z+j,"air")
        
        for i in range(-4,4):
            for j in range(-4,4):
                INTF.placeBlock(x+i,y-1,z+j,"oak_planks")


    size = 6
    roof = np.zeros((size,size))
    for m in range(0,len(roof)//2):
        for i in range(m,len(roof)-m):
            for j in range(m,len(roof[0])-m):
                if (i == 0+m):
                    roof[i][j] = m
                elif (i == len(roof)-1-m):
                    roof[i][j] = m
                elif (j == 0+m):
                    roof[i][j] = m
                elif (j == len(roof[0])-1-m):
                    roof[i][j] = m
    roof[size//2][size//2] = roof[(size//2)-1][size//2]
    h = 2
    for tx in range(0,len(roof[0])):
        for ty in range(0,len(roof)):
            v = int(roof[ty][tx])
            if (tx == 0 and ty == 0) or (tx == 0 and ty == size-1) or (tx == size-1 and ty == 0) or (tx == size-1 and ty == size-1):
                GEO.placeCuboid(X+tx+4, y + 2 + h + v, Z+ty+4, X+tx+4, y + 2 + h + v, Z+ty+4,"lantern"+"[hanging=false]")
                INTF.placeBlock(X+tx+4, y , Z+ty+4,"spruce_fence")
                INTF.placeBlock(X+tx+4, y+1 , Z+ty+4,"spruce_fence")
                INTF.placeBlock(X+tx+4, y+2 , Z+ty+4,"spruce_fence")
            GEO.placeCuboid(X + tx+4, y + 1 + h + v, Z + ty+4, X + tx+4, y + 1 + h + v, Z + ty+4, "spruce_planks")
        
    for p in dir:
        INTF.runCommand(f"summon boat {p[0]} {y} {p[1]}")

    
    
    
    
    
    

