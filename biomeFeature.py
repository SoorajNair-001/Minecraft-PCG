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

# well
def deserts(x,Y,z):
    Y=Y+1
    size = 15
    X = x-(size//2)
    Z = z-(size//2)
    fgrid = np.zeros((size,size))

    for i in range((len(fgrid)//2)-2,(len(fgrid)//2)+3):
        for j in range((len(fgrid)//2)-2,(len(fgrid)//2)+3):
                fgrid[i][j] = 7
                
    for i in range(0,len(fgrid)):
        for j in range(0,len(fgrid[0])):
            if fgrid[i][j] == 0:
                INTF.placeBlock(X+i, Y-1, Z+j, "stone_bricks")
                INTF.placeBlock(X+i, Y-2, Z+j, "stone_bricks")
                INTF.placeBlock(X+i, Y-3, Z+j, "stone_bricks")
                INTF.placeBlock(X+i, Y-4, Z+j, "stone_bricks")
                INTF.placeBlock(X+i, Y-5, Z+j, "stone_bricks")
                INTF.placeBlock(X+i, Y-6, Z+j, "stone_bricks")
                INTF.placeBlock(X+i, Y-7, Z+j, "stone_bricks")
            if fgrid[i][j] == 7:
                INTF.placeBlock(X+i, Y-1, Z+j, "water")
                INTF.placeBlock(X+i, Y-2, Z+j, "water")
                INTF.placeBlock(X+i, Y-3, Z+j, "water")
                INTF.placeBlock(X+i, Y-4, Z+j, "water")
                INTF.placeBlock(X+i, Y-5, Z+j, "water")
                INTF.placeBlock(X+i, Y-6, Z+j, "water")
                INTF.placeBlock(X+i, Y-7, Z+j, "stone_bricks")
    
    for i in range((len(fgrid)//2)-2,(len(fgrid)//2)+3):
        for j in range((len(fgrid)//2)-2,(len(fgrid)//2)+3):
            if i == (len(fgrid)//2)-2 or i == (len(fgrid)//2)+2 or j == (len(fgrid)//2)-2 or j == (len(fgrid)//2)+2 :
                INTF.placeBlock(X+i, Y, Z+j, "stone_bricks")
                if i == (len(fgrid)//2)-2 and j == (len(fgrid)//2)-2:
                    INTF.placeBlock(X+i, Y+1, Z+j, "oak_fence")
                    INTF.placeBlock(X+i, Y+2, Z+j, "oak_fence")
                if i == (len(fgrid)//2)+2 and j == (len(fgrid)//2)-2:
                    INTF.placeBlock(X+i, Y+1, Z+j, "oak_fence")
                    INTF.placeBlock(X+i, Y+2, Z+j, "oak_fence")
                if i == (len(fgrid)//2)-2 and j == (len(fgrid)//2)+2:
                    INTF.placeBlock(X+i, Y+1, Z+j, "oak_fence")
                    INTF.placeBlock(X+i, Y+2, Z+j, "oak_fence")
                if i == (len(fgrid)//2)+2 and j == (len(fgrid)//2)+2:
                    INTF.placeBlock(X+i, Y+1, Z+j, "oak_fence")
                    INTF.placeBlock(X+i, Y+2, Z+j, "oak_fence")
    
    size = 5
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
                GEO.placeCuboid(X+tx+5, Y + 2 + h + v, Z+ty+5, X+tx+5, Y + 2 + h + v, Z+ty+5,"lantern"+"[hanging=false]")
            GEO.placeCuboid(X + tx+5, Y + 1 + h + v, Z + ty+5, X + tx+5, Y + 1 + h + v, Z + ty+5, "spruce_planks")

# underwater view
def oceans(x,Y,z):
    size = 15
    X = x-(size//2)
    Z = z-(size//2)
    fgrid = np.zeros((size,size))
    for i in range(0,len(fgrid)):
        for j in range(0,len(fgrid[0])):
            if i == 0 or i == len(fgrid)-1 or j == 0 or j == len(fgrid[0])-1:
                for yy in range(0,7):
                    INTF.placeBlock(X+i,Y-yy,Z+j,"glass")
            else:
                for yy in range(0,7):
                    INTF.placeBlock(X+i,Y-yy,Z+j,"air")
    for i in range(0,len(fgrid)):
        for j in range(0,len(fgrid[0])):
            if i == 1 or i == len(fgrid)-2 or j == 1 or j == len(fgrid[0])-2:
                for yy in range(0,5):
                    INTF.placeBlock(X+i,Y+yy,Z+j,"glass")
            else:
                for yy in range(0,5):
                    INTF.placeBlock(X+i,Y+yy,Z+j,"air")
    opening = "air"
    INTF.placeBlock(X+1,Y+1,Z+(size//2)-1,opening)
    INTF.placeBlock(X+1,Y+1,Z+(size//2),opening)
    INTF.placeBlock(X+1,Y+1,Z+(size//2)+1,opening)
    INTF.placeBlock(X+1,Y+2,Z+(size//2)-1,opening)
    INTF.placeBlock(X+1,Y+2,Z+(size//2),opening)
    INTF.placeBlock(X+1,Y+2,Z+(size//2)+1,opening)
    INTF.placeBlock(X+1,Y+3,Z+(size//2)-1,opening)
    INTF.placeBlock(X+1,Y+3,Z+(size//2),opening)
    INTF.placeBlock(X+1,Y+3,Z+(size//2)+1,opening)

    INTF.placeBlock(X+(size//2)-1,Y+1,Z+1,opening)
    INTF.placeBlock(X+(size//2),Y+1,Z+1,opening)
    INTF.placeBlock(X+(size//2)+1,Y+1,Z+1,opening)
    INTF.placeBlock(X+(size//2)-1,Y+2,Z+1,opening)
    INTF.placeBlock(X+(size//2),Y+2,Z+1,opening)
    INTF.placeBlock(X+(size//2)+1,Y+2,Z+1,opening)
    INTF.placeBlock(X+(size//2)-1,Y+3,Z+1,opening)
    INTF.placeBlock(X+(size//2),Y+3,Z+1,opening)
    INTF.placeBlock(X+(size//2)+1,Y+3,Z+1,opening)

    INTF.placeBlock(X+13,Y+1,Z+(size//2)-1,opening)
    INTF.placeBlock(X+13,Y+1,Z+(size//2),opening)
    INTF.placeBlock(X+13,Y+1,Z+(size//2)+1,opening)
    INTF.placeBlock(X+13,Y+2,Z+(size//2)-1,opening)
    INTF.placeBlock(X+13,Y+2,Z+(size//2),opening)
    INTF.placeBlock(X+13,Y+2,Z+(size//2)+1,opening)
    INTF.placeBlock(X+13,Y+3,Z+(size//2)-1,opening)
    INTF.placeBlock(X+13,Y+3,Z+(size//2),opening)
    INTF.placeBlock(X+13,Y+3,Z+(size//2)+1,opening)

    INTF.placeBlock(X+(size//2)-1,Y+1,Z+13,opening)
    INTF.placeBlock(X+(size//2),Y+1,Z+13,opening)
    INTF.placeBlock(X+(size//2)+1,Y+1,Z+13,opening)
    INTF.placeBlock(X+(size//2)-1,Y+2,Z+13,opening)
    INTF.placeBlock(X+(size//2),Y+2,Z+13,opening)
    INTF.placeBlock(X+(size//2)+1,Y+2,Z+13,opening)
    INTF.placeBlock(X+(size//2)-1,Y+3,Z+13,opening)
    INTF.placeBlock(X+(size//2),Y+3,Z+13,opening)
    INTF.placeBlock(X+(size//2)+1,Y+3,Z+13,opening)




    for i in range(0,len(fgrid)):
        for j in range(0,len(fgrid[0])):
            if i == 0 and j == 0:
                GEO.placeCuboid(X+i, Y-7, Z+j, X+i, Y-7, Z+j, "sea_lantern")
            elif i == 0 and j == len(fgrid[0])-1:
                GEO.placeCuboid(X+i, Y-7, Z+j, X+i, Y-7, Z+j, "sea_lantern")
            elif i == len(fgrid)-1 and j == 0:
                GEO.placeCuboid(X+i, Y-7, Z+j, X+i, Y-7, Z+j, "sea_lantern")
            elif i == len(fgrid)-1 and j == len(fgrid[0])-1:
                GEO.placeCuboid(X+i, Y-7, Z+j, X+i, Y-7, Z+j, "sea_lantern")
            else:
                GEO.placeCuboid(X+i, Y-7, Z+j, X+i, Y-7, Z+j, "glass")

    
    for i in range(0,len(fgrid)):
        for j in range(0,len(fgrid[0])):
            GEO.placeCuboid(X+i, Y, Z+j, X+i, Y, Z+j, "stone_bricks")
    for i in range((len(fgrid)//2)-2,(len(fgrid)//2)+2):
        for j in range((len(fgrid[0])//2)-2,(len(fgrid[0])//2)+2):
            INTF.placeBlock(X+i,Y,Z+j,"air")
    for i in range(0,len(fgrid)-1):
        for yy in range(0,7):
            INTF.placeBlock(X+6,Y-yy,Z+8,"ladder")
    
    size = 15
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
                GEO.placeCuboid(X+tx+0, Y + 3 + h + v, Z+ty+0, X+tx+0, Y + 3 + h + v, Z+ty+3,"lantern"+"[hanging=false]")
                GEO.placeCuboid(X+tx+0, Y + 3 + h + v -1, Z+ty+0, X+tx+0, Y + 3 + h + v -1, Z+ty+0,"oak_fence")
                GEO.placeCuboid(X+tx+0, Y + 3 + h + v -2, Z+ty+0, X+tx+0, Y + 3 + h + v -2, Z+ty+0,"oak_fence")
                GEO.placeCuboid(X+tx+0, Y + 3 + h + v -3, Z+ty+0, X+tx+0, Y + 3 + h + v -3, Z+ty+0,"oak_fence")
                GEO.placeCuboid(X+tx+0, Y + 3 + h + v -4, Z+ty+0, X+tx+0, Y + 3 + h + v -4, Z+ty+0,"oak_fence")
                
            GEO.placeCuboid(X + tx+0, Y + 2 + h + v, Z + ty+0, X + tx+0, Y + 2 + h + v, Z + ty+0, "spruce_planks")

# wood mill
def taiga_forest(x,Y,z):
    size = 15
    X = x-(size//2)
    Z = z-(size//2)
    fgrid = np.zeros((size,size))

    for i in range(0,len(fgrid)):
        for j in range(0,len(fgrid[0])):
            GEO.placeCuboid(X+i, Y, Z+j, X+i, Y, Z+j, "stone_bricks")
    

    for zz in range(5,10):
        fgrid[2][zz] = 1
        fgrid[3][zz] = 2
        fgrid[4][zz] = 3
        fgrid[5][zz] = 2
        fgrid[6][zz] = 1
    fgrid[6][10] = 6
    fgrid[5][10] = 6
    fgrid[5][4] = 6
    
    
    for zz in range(2,13):
        fgrid[13][zz] = 5
    for xx in range(8,13):
        fgrid[xx][2] = 5
        fgrid[xx][12] = 5
    

    for i in range(0,len(fgrid)):
        for j in range(0,len(fgrid[0])):
            if fgrid[i][j] == 1 or fgrid[i][j] == 2 or fgrid[i][j] == 3:
                for yy in range(0,int(fgrid[i][j])):
                    INTF.placeBlock(X+i,Y+yy+1,Z+j,"spruce_log"+"[axis=z]")
            elif fgrid[i][j] == 6:
                INTF.placeBlock(X+i,Y+1,Z+j,"spruce_log")
            elif fgrid[i][j] == 5:
                for yy in range(0,6):
                    INTF.placeBlock(X+i,Y+yy+1,Z+j,"oak_wood")
    INTF.placeBlock(X+2,Y+2,Z+6,"spruce_log")
    
    for zz in range(1,14):
        yy = 3
        INTF.placeBlock(X+13,Y+1+yy,Z+zz,"oak_planks")
        INTF.placeBlock(X+13,Y+1+yy+1,Z+zz,"air")
        INTF.placeBlock(X+13,Y+1+yy+2,Z+zz,"air")
        INTF.placeBlock(X+12,Y+2+yy,Z+zz,"oak_planks")
        INTF.placeBlock(X+12,Y+2+yy+1,Z+zz,"air")
        INTF.placeBlock(X+11,Y+3+yy,Z+zz,"oak_planks")
        INTF.placeBlock(X+10,Y+4+yy,Z+zz,"oak_planks")
        INTF.placeBlock(X+9,Y+4+yy,Z+zz,"oak_planks")
        INTF.placeBlock(X+8,Y+4+yy,Z+zz,"oak_planks")
        INTF.placeBlock(X+7,Y+4+yy,Z+zz,"oak_planks")
    

    INTF.placeBlock(X+12,Y+1,Z+4,"spruce_log")
    INTF.placeBlock(X+11,Y+1,Z+6,"spruce_planks")
    INTF.placeBlock(X+11,Y+1,Z+10,"spruce_planks")
    INTF.placeBlock(X+12,Y+1,Z+5,"stonecutter"+"[facing=west]")
    INTF.placeBlock(X+11,Y+1,Z+5,"stonecutter"+"[facing=west]")
    INTF.placeBlock(X+10,Y+1,Z+5,"stonecutter"+"[facing=west]")
    INTF.placeBlock(X+9,Y+1,Z+5,"stonecutter"+"[facing=west]")
    INTF.placeBlock(X+12,Y+1,Z+9,"stonecutter"+"[facing=west]")
    INTF.placeBlock(X+10,Y+1,Z+10,"spruce_log")
    INTF.placeBlock(X+11,Y+1,Z+9,"stonecutter"+"[facing=west]")
    INTF.placeBlock(X+10,Y+1,Z+9,"stonecutter"+"[facing=west]")
    INTF.placeBlock(X+9,Y+1,Z+9,"stonecutter"+"[facing=west]")
    INTF.placeBlock(X+7,Y+6,Z+13,"lantern"+"[hanging=true]")
    INTF.placeBlock(X+7,Y+6,Z+1,"lantern"+"[hanging=true]")

# igloo
def snowy_tundra(x,Y,z):
    size = 15
    X = x-(size//2)
    Z = z-(size//2)
    fgrid = np.zeros((size,size))

    for i in range(0,len(fgrid)):
        for j in range(0,len(fgrid[0])):
            GEO.placeCuboid(X+i, Y, Z+j, X+i, Y, Z+j, "snow_block")

    GEO.placeCenteredCylinder(x,Y+1,z, 1, 6, "snow_block")
    GEO.placeCenteredCylinder(x,Y+1,z, 1, 5, "air")
    GEO.placeCenteredCylinder(x,Y+2,z, 1, 6, "snow_block")
    GEO.placeCenteredCylinder(x,Y+2,z, 1, 5, "air")
    INTF.placeBlock(x,Y+1,z+5,"air")
    INTF.placeBlock(x,Y+2,z+5,"air")

    INTF.placeBlock(x+1,Y+1,z+6,"snow_block")
    INTF.placeBlock(x-1,Y+1,z+6,"snow_block")
    INTF.placeBlock(x+1,Y+2,z+6,"snow_block")
    INTF.placeBlock(x-1,Y+2,z+6,"snow_block")

    INTF.placeBlock(x,Y+3,z+5,"snow_block")
    INTF.placeBlock(x,Y+3,z+6,"snow_block")


    GEO.placeCenteredCylinder(x,Y+3,z, 1, 5, "snow_block")
    GEO.placeCenteredCylinder(x,Y+3,z, 1, 4, "air")
    GEO.placeCenteredCylinder(x,Y+4,z, 1, 5, "snow_block")
    GEO.placeCenteredCylinder(x,Y+4,z, 1, 4, "air")

    GEO.placeCenteredCylinder(x,Y+5,z, 1, 4, "snow_block")
    GEO.placeCenteredCylinder(x,Y+5,z, 1, 3, "air")

    GEO.placeCenteredCylinder(x,Y+6,z, 1, 3, "snow_block")

    INTF.runCommand(f"summon snow_golem {X+1} {Y+1} {Z+1}")
    INTF.runCommand(f"summon snow_golem {X+13} {Y+1} {Z+1}")
    INTF.placeBlock(x,Y+1,z,"campfire")
    INTF.placeBlock(x,Y+6,z,"air")



        



            