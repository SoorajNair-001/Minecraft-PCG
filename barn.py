from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL

import random
STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()

WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)
import numpy as np

size = 15

def buildBarn(x,Y,z,biome):
    Y +=1
    X = x-(size//2)
    Z = z-(size//2)
    fgrid = np.zeros((size,size))

    # blocks for biomes
    if 'desert' in biome:
        foundation = "sandstone"
        roofBlock = "red_sandstone"
        accentBlock = "oak_planks"

    elif 'ocean' in biome:
        foundation = "glass"
        roofBlock = "sea_lantern"
        accentBlock = "oak_planks"

    elif 'forest' in biome:
        foundation = "infested_mossy_stone_bricks"
        roofBlock = "dark_oak_planks"
        accentBlock = "oak_planks"

    elif 'taiga' in biome:
        foundation = "infested_mossy_stone_bricks"
        roofBlock = "dark_oak_planks"
        accentBlock = "oak_planks"

    elif 'snowy' in biome:
        foundation = "snow_block"
        roofBlock = "snow_block"
        accentBlock = "oak_planks"

    # build base
    for i in range(-2,len(fgrid)+2):
        for j in range(-2,len(fgrid[0])+2):
            GEO.placeCuboid(X+i, Y-1, Z+j, X+i, Y-1, Z+j, foundation)

    # creating main Layout grid
    for i in range(0,len(fgrid)):
        for j in range(0,len(fgrid[0])):
            if (i == 0):
                fgrid[i][j] = 1
            elif (i == len(fgrid)-1):
                fgrid[i][j] = 1
            elif (j == 0):
                fgrid[i][j] = 1
            elif (j == len(fgrid[0])-1):
                fgrid[i][j] = 1

    fgrid[(len(fgrid)//2)-3][len(fgrid)-1] = 7
    fgrid[(len(fgrid)//2)-2][len(fgrid)-1] = 2
    fgrid[(len(fgrid)//2)-1][len(fgrid)-1] = 2
    fgrid[(len(fgrid)//2)][len(fgrid)-1] = 2
    fgrid[(len(fgrid)//2)+1][len(fgrid)-1] = 2
    fgrid[(len(fgrid)//2)+2][len(fgrid)-1] = 7

    fgrid[1][1] = 3
    fgrid[len(fgrid)-2][1] = 3
    fgrid[1][len(fgrid)-2] = 3
    fgrid[len(fgrid)-2][len(fgrid)-2] = 3
    fgrid[len(fgrid)//2][len(fgrid)//2] = 4
    fgrid[len(fgrid)//2][1] = 4
    fgrid[1][len(fgrid)//2] = 3
    fgrid[len(fgrid)-2][len(fgrid)//2] = 3
    
    # placing blocks using the layout grid
    for yy in range(0,5):
        for i in range(0,len(fgrid)):
            for j in range(0,len(fgrid[0])):
                if fgrid[i][j] == 1:
                    GEO.placeCuboid(X+i, Y+yy, Z+j, X+i, Y+yy, Z+j, "acacia_planks")
                if fgrid[i][j] == 7:
                    GEO.placeCuboid(X+i, Y+yy, Z+j, X+i, Y+yy, Z+j, accentBlock)
    for i in range(0,len(fgrid)):
            for j in range(0,len(fgrid[0])):
                yy = 5
                if fgrid[i][j] == 2 or fgrid[i][j] == 7:
                    GEO.placeCuboid(X+i, Y+yy, Z+j, X+i, Y+yy, Z+j, accentBlock)
                elif fgrid[i][j] == 1:
                    GEO.placeCuboid(X+i, Y+yy, Z+j, X+i, Y+yy, Z+j, "glass")
    for yy in range(6,10):
        for i in range(0,len(fgrid)):
            for j in range(0,len(fgrid[0])):
                if fgrid[i][j] == 1 or fgrid[i][j] == 2 or fgrid[i][j] == 7:
                    GEO.placeCuboid(X+i, Y+yy, Z+j, X+i, Y+yy, Z+j, "acacia_planks")
    
    # roof layout 
    roof = [[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0],
            [0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0],
            [0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
            [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]]

    # placing roof blocks
    for zz in range(-1,16):   
        for i in range(0,len(roof)):
            for j in range(0,len(roof[0])):
                if roof[i][j] ==1:
                    INTF.placeBlock(X+j-1, Y-i+10, Z+zz,roofBlock)
                    if i!=len(roof)-1:
                        INTF.placeBlock(X+j-1, Y-i+11, Z+zz,"air")
                        INTF.placeBlock(X+j-1, Y-i+12, Z+zz,"air")
                        INTF.placeBlock(X+j-1, Y-i+13, Z+zz,"air")
                        INTF.placeBlock(X+j-1, Y-i+14, Z+zz,"air")
                        INTF.placeBlock(X+j-1, Y-i+15, Z+zz,"air")

    for i in range(0,len(fgrid)):
            for j in range(0,len(fgrid[0])):
                if fgrid[i][j] == 3:
                    INTF.placeBlock(X+i, Y+6, Z+j,"lantern"+"[hanging=true]")
                if fgrid[i][j] == 4:
                    INTF.placeBlock(X+i, Y+9, Z+j,"lantern"+"[hanging=true]")

    # plcing fence
    for i in range(1,(len(fgrid)//2)-2):
        for j in range(1,len(fgrid)-1):
            if j==7:
                GEO.placeCuboid(X+i, Y, Z+j, X+i, Y, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
                GEO.placeCuboid(X+i, Y+1, Z+j, X+i, Y+1, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
            if i==4:
                GEO.placeCuboid(X+i, Y, Z+j, X+i, Y, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
                GEO.placeCuboid(X+i, Y+1, Z+j, X+i, Y+1, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
    for i in range(1,(len(fgrid)//2)-2):
        for j in range(1,len(fgrid)-1):
            if j==7:
                GEO.placeCuboid(X+i, Y, Z+j, X+i, Y, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
                GEO.placeCuboid(X+i, Y+1, Z+j, X+i, Y+1, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
            if i==4:
                GEO.placeCuboid(X+i, Y, Z+j, X+i, Y, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
                GEO.placeCuboid(X+i, Y+1, Z+j, X+i, Y+1, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
    
    for i in range((len(fgrid)//2)+2,len(fgrid)-1):
        for j in range(1,len(fgrid)-1):
            if j==7:
                GEO.placeCuboid(X+i, Y, Z+j, X+i, Y, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
                GEO.placeCuboid(X+i, Y+1, Z+j, X+i, Y+1, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
            if i==9:
                GEO.placeCuboid(X+i, Y, Z+j, X+i, Y, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
                GEO.placeCuboid(X+i, Y+1, Z+j, X+i, Y+1, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
    for i in range((len(fgrid)//2)+2,len(fgrid)-1):
        for j in range(1,len(fgrid)-1):
            if j==7:
                GEO.placeCuboid(X+i, Y, Z+j, X+i, Y, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
                GEO.placeCuboid(X+i, Y+1, Z+j, X+i, Y+1, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
            if i==9:
                GEO.placeCuboid(X+i, Y, Z+j, X+i, Y, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
                GEO.placeCuboid(X+i, Y+1, Z+j, X+i, Y+1, Z+j, "oak_fence"+"[north=true,south=true,east=true,west=true]")

    # place animals in the barn
    r = random.randint(0,400)
    if r<=100:
        command1 = f"summon horse {X+3} {Y} {Z+3}"
        command2 = f"summon horse {X+3} {Y} {Z+11}"
        command3 = f"summon horse {X+11} {Y} {Z+3}"
        command4 = f"summon horse {X+11} {Y} {Z+11}"
    elif r>100 and r<=200:
        command1 = f"summon cow {X+3} {Y} {Z+3}"
        command2 = f"summon cow {X+3} {Y} {Z+11}"
        command3 = f"summon cow {X+11} {Y} {Z+3}"
        command4 = f"summon cow {X+11} {Y} {Z+11}"
    elif r>200 and r<=300:
        command1 = f"summon sheep {X+3} {Y} {Z+3}"
        command2 = f"summon sheep {X+3} {Y} {Z+11}"
        command3 = f"summon sheep {X+11} {Y} {Z+3}"
        command4 = f"summon sheep {X+11} {Y} {Z+11}"
    elif r>300 and r<=400:
        command1 = f"summon pig {X+3} {Y} {Z+3}"
        command2 = f"summon pig {X+3} {Y} {Z+11}"
        command3 = f"summon pig {X+11} {Y} {Z+3}"
        command4 = f"summon pig {X+11} {Y} {Z+11}"

    for i in range(0,5):
        INTF.runCommand(command1)
        INTF.runCommand(command2)
        INTF.runCommand(command3)
        INTF.runCommand(command4)


