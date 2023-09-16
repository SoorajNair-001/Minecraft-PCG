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
size = 15
def buildFarm(x,Y,z):
    X = x-(size//2)
    Z = z-(size//2)
    fgrid = np.zeros((size,size))
    # base
    for i in range(-2,len(fgrid)+2):
        for j in range(-2,len(fgrid[0])+2):
            GEO.placeCuboid(X+i, Y, Z+j, X+i, Y, Z+j, "grass_path")

    # layout grid
    for i in range(0,len(fgrid)//3):
        for j in range(0,len(fgrid[0])//3):
            fgrid[i][j] = 1
    for i in range(len(fgrid)//3,len(fgrid)//3+len(fgrid)//3):
        for j in range(0,len(fgrid[0])//3):
            fgrid[i][j] = 2
    for i in range(len(fgrid)//3+len(fgrid)//3,len(fgrid)):
        for j in range(0,len(fgrid[0])//3):
            fgrid[i][j] = 1
    
    for i in range(0,len(fgrid)//3):
        for j in range(len(fgrid)//3,len(fgrid[0])//3+len(fgrid)//3):
            fgrid[i][j] = 2
    for i in range(len(fgrid)//3,len(fgrid)//3+len(fgrid)//3):
        for j in range(len(fgrid)//3,len(fgrid[0])//3+len(fgrid)//3):
            fgrid[i][j] = 0
    for i in range(len(fgrid)//3+len(fgrid)//3,len(fgrid)):
        for j in range(len(fgrid)//3,len(fgrid[0])//3+len(fgrid)//3):
            fgrid[i][j] = 2
    
    for i in range(0,len(fgrid)//3):
        for j in range(len(fgrid)//3+len(fgrid)//3,len(fgrid[0])):
            fgrid[i][j] = 1
    for i in range(len(fgrid)//3,len(fgrid)//3+len(fgrid)//3):
        for j in range(len(fgrid)//3+len(fgrid)//3,len(fgrid[0])):
            fgrid[i][j] = 2
    for i in range(len(fgrid)//3+len(fgrid)//3,len(fgrid)):
        for j in range(len(fgrid)//3+len(fgrid)//3,len(fgrid[0])):
            fgrid[i][j] = 1

    # placing blocks
    for i in range(0,len(fgrid)):
        for j in range(0,len(fgrid[0])):
            if fgrid[i][j] == 0:
                INTF.placeBlock(X+i, Y, Z+j, "water")
                INTF.placeBlock(X+i, Y+1, Z+j, "water")
    for i in range(0,len(fgrid)):
        for j in range(0,len(fgrid[0])):
            if fgrid[i][j] == 1:
                INTF.placeBlock(X+i, Y+1, Z+j, "farmland"+"[moisture=7]")
                INTF.placeBlock(X+i, Y+2, Z+j, "wheat"+"[age=7]")
            if fgrid[i][j] == 2:
                INTF.placeBlock(X+i, Y+1, Z+j, "farmland"+"[moisture=7]")
                INTF.placeBlock(X+i, Y+2, Z+j, "carrots"+"[age=7]")

    