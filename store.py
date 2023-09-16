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


def buildStore(x,Y,z,biome):
    Y+=1
    X = x-(15//2)
    Z = z-(15//2)
    fgrid = np.zeros((15,10))
    carpets = ["blue_carpet","cyan_carpet","red_carpet","white_carpet","purple_carpet","lime_carpet","orange_carpet"]
    plants = ["oak_sapling","spruce_sapling","birch_sapling","acacia_sapling","jungle_sapling","dark_oak_sapling"]
    flowers = ["poppy","blue_orchid","oxeye_daisy","allium","dandelion"]
    carpets = ["blue_carpet","cyan_carpet","red_carpet","white_carpet","purple_carpet","lime_carpet","orange_carpet"]
    r_carp = random.randint(0,len(carpets)-1)
    r = random.randint(0,300)

    #  biome blocks
    if 'desert' in biome:
        foundation = "sandstone"
        mainBlock = "red_sandstone"
    elif 'ocean' in biome:
        foundation = "glass"
        mainBlock = "prismarine_bricks"
    elif 'forest' in biome:
        foundation = "infested_mossy_stone_bricks"
        mainBlock = "infested_mossy_stone_bricks"
    elif 'taiga' in biome:
        foundation = "stone_bricks"
        mainBlock = "stone_bricks"
    elif 'snowy' in biome:
        foundation = "snow_block"
        mainBlock = "chiseled_quartz_block"

    # base
    for i in range(-2,len(fgrid)+2):
        for j in range(-2,len(fgrid[0])+2):
            GEO.placeCuboid(X+i, Y-1, Z+j, X+i, Y-1, Z+j, foundation)

    # layout grid
    for i in range(0,len(fgrid)):
        for j in range(0,len(fgrid[0])):
            if i == 0 or i == len(fgrid)-1 or j == 0 or j == len(fgrid[0])-1:
                fgrid[i][j] = 1
                if (i == 0 and j == 0) or (i == 0 and j == 9) or (i == 14 and j == 0) or (i == 14 and j == 9):
                    fgrid[i][j] = 2
    fgrid[9][9] = 5
    fgrid[10][9] = 5

    fgrid[10][5] = 6
    fgrid[10][4] = 6
    fgrid[12][4] = 7
    fgrid[10][3] = 6
    fgrid[11][5] = 6
    fgrid[12][5] = 6
    fgrid[13][5] = 6

    for i in range(1,8,2):
        for j in range(1,6):
            fgrid[i][j] = 20
    
    # place blocks
    for i in range(1,len(fgrid)-1):
        for j in range(1,len(fgrid[0])-1):
            INTF.placeBlock(X+i, Y, Z+j, carpets[r_carp])
    for i in range(0,len(fgrid)):
        for j in range(0,len(fgrid[0])):
            if fgrid[i][j]==1 or fgrid[i][j]==2:
                GEO.placeCuboid(X+i, Y, Z+j, X+i, Y, Z+j, mainBlock)
    for i in range(1,len(fgrid)-1):
        for j in range(1,len(fgrid[0])-1):
            INTF.placeBlock(X+i, Y, Z+j, carpets[r_carp])
    for i in range(0,len(fgrid)):
        for j in range(0,len(fgrid[0])):
            if fgrid[i][j]==6:
                INTF.placeBlock(X+i, Y, Z+j, "oak_planks")
            if fgrid[i][j]==7:
                INTF.runCommand(f"summon wandering_trader {X+i} {Y} {Z+j}")
            if fgrid[i][j]==20:
                if r <=100:
                    INTF.placeBlock(X+i, Y, Z+j, "bookshelf")
                    INTF.placeBlock(X+i, Y+1, Z+j, "bookshelf")
                    INTF.placeBlock(X+i, Y+2, Z+j, "bookshelf")
                elif r > 100 and r <= 200:
                    r_plant = random.randint(0,len(plants)-1)
                    INTF.placeBlock(X+i, Y, Z+j, "dirt")
                    INTF.placeBlock(X+i, Y+1, Z+j, plants[r_plant])
                elif r > 200 and r <= 300:
                    r_flower = random.randint(0,len(flowers)-1)
                    INTF.placeBlock(X+i, Y, Z+j, "dirt")
                    INTF.placeBlock(X+i, Y+1, Z+j, flowers[r_flower])

    INTF.runCommand(f"summon villager {x} {Y} {z}")
    INTF.runCommand(f"summon villager {x+2} {Y} {z}")

    for yy in range(1,5):
        for i in range(0,len(fgrid)):
            for j in range(0,len(fgrid[0])):
                if fgrid[i][j]==2:
                    GEO.placeCuboid(X+i, Y+yy, Z+j, X+i, Y+yy, Z+j, mainBlock)
                elif fgrid[i][j]==1:
                    GEO.placeCuboid(X+i, Y+yy, Z+j, X+i, Y+yy, Z+j, "glass")
    
    for i in range(-1,len(fgrid)+1):
        for j in range(-1,len(fgrid[0])+1):
            GEO.placeCuboid(X+i, Y+5, Z+j, X+i, Y+5, Z+j, mainBlock)

    
    # top banner
    banner = [[1,1,1,0,1,0,1,0,0,1,0,0,1,1,1],
              [1,0,0,0,1,0,1,0,1,0,1,0,1,0,1],
              [1,1,1,0,1,1,1,0,1,0,1,0,1,1,1],
              [0,0,1,0,1,0,1,0,1,0,1,0,1,0,0],
              [1,1,1,0,1,0,1,0,0,1,0,0,1,0,0]]
    banner.reverse()
    for i in range(0,len(banner)):
        for j in range(0,len(banner[0])):
            if banner[i][j] == 1:
                INTF.placeBlock(X+j, Y+5+i, Z+10, "sea_lantern")
    


