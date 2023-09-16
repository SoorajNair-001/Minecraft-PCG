import numpy as np
from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL
import random

STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()
WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)


#Y = heights[(X,Z)]
def buildLHouse(X,Y,Z,biome):
    X = X-(15//2)
    Z = Z-(15//2)
    r = random.randint(0,1)

    # biome blocks
    if r == 0: mainBlock = "oak_planks"
    elif r == 1: mainBlock = "bricks"
    if 'desert' in biome:
        foundation = "sandstone"
        foundationBlockBorder = "sandstone"
        accentBlock = "red_sandstone"
        roofStairs = "red_sandstone_stairs"
        roofStairs2 = "red_sandstone_stairs"
        slab = "red_sandstone_slab"
    elif 'ocean' in biome:
        foundation = "glass"
        foundationBlockBorder = "glass"
        accentBlock = "sea_lantern"
        roofStairs = "prismarine_brick_stairs"
        roofStairs2 = "prismarine_brick_stairs"
        slab = "prismarine_brick_slab"
    elif 'forest' in biome:
        foundation = "infested_mossy_stone_bricks"
        foundationBlockBorder = "chiseled_stone_bricks"
        accentBlock = "spruce_planks"
        roofStairs = "spruce_stairs"
        roofStairs2 = "dark_oak_slab"
        slab = "dark_oak_slab"
    elif 'taiga' in biome:
        foundation = "infested_mossy_stone_bricks"
        foundationBlockBorder = "chiseled_stone_bricks"
        accentBlock = "spruce_planks"
        roofStairs = "spruce_stairs"
        roofStairs2 = "dark_oak_slab"
        slab = "dark_oak_slab"
    elif 'snowy' in biome:
        foundation = "snow_block"
        foundationBlockBorder = "snow_block"
        accentBlock = "snow_block"
        roofStairs = "quartz_stairs"
        roofStairs2 = "quartz_stairs"
        slab = "quartz_slab"

    # decorations
    flowers = ["poppy","blue_orchid","oxeye_daisy","allium","dandelion"]
    carpets = ["blue_carpet","cyan_carpet","red_carpet","white_carpet","purple_carpet","lime_carpet","orange_carpet"]
    beds = ["blue_bed","cyan_bed","red_bed","white_bed","purple_bed","lime_bed","orange_bed"]
    seats = ["prismarine_stairs","red_nether_brick_stairs","smooth_quartz_stairs","crimson_stairs"]
    items = ["chest","ender_chest","smoker","furnace"]
    itemsNodir = ["smithing_table","composter","cartography_table","fletching_table"]

    r_carp = random.randint(0,len(carpets)-1)
    r_bed = random.randint(0,len(carpets)-1)
    r_seat = random.randint(0,len(seats)-1)

    r1 = random.randint(0,100)
    if r1 < 50: dir = "s"
    else: dir = "n"

    # layout template
    size = 15
    templateL = [[-13,0,0,0,0,0,0,0,0,0,0,0,0,0,-13],
                [0,1,1,1,1,1,1,-2,-2,-2,1,1,1,1,0],
                [0,1,-7,-7,-6,-5,-1,9,9,9,9,9,-20,1,0],
                [0,1,-7,-7,-6,-5,-1,9,9,9,9,9,-31,1,0],
                [0,1,-7,-7,-6,-5,-1,9,9,9,9,9,-32,-2,0],
                [0,-2,9,9,9,9,9,9,9,9,9,9,9,-2,0],
                [0,-2,9,9,9,9,9,9,9,9,9,9,9,-2,0],
                [0,-2,9,9,9,9,9,9,9,9,9,9,9,1,0],
                [0,1,9,9,9,9,9,9,9,9,9,9,-20,1,0],
                [0,1,5,6,6,6,6,5,1,1,1,2,3,1,0],
                [0,4,8,8,8,8,8,8,4,-9,-11,-11,-11,-9,-10],
                [0,4,8,8,8,8,8,8,4,-9,-10,-10,-10,-9,-10],
                [0,4,-21,8,8,8,8,-21,4,-9,-10,-10,-10,-9,-10],
                [0,4,4,7,7,7,7,4,4,-9,-9,-10,-10,-9,-10],
                [-13,0,0,0,0,0,0,0,-13,-10,-10,-10,-10,-10,-10]]
    

    interiorL = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,11,0,0,0,0,0,0,5,0,6,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,7,0,0,0,0,0,0,0,0,0,9,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,4,0,0,0,0,0,0,0,0,0,8,0,0],
                 [0,0,12,0,0,0,0,0,0,10,0,0,0,0,0],
                 [0,0,1,0,3,3,0,2,0,0,0,0,0,0,0],
                 [0,0,1,0,3,3,0,2,0,0,0,0,0,0,0],
                 [0,0,1,0,3,3,0,2,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],]

    # placing blocks    
    for i in range(-2,len(templateL)+2):
        for j in range(-2,len(templateL)+2):
            if i == -2 or j == -2 or i == size+1 or j == size+1:
                GEO.placeCuboid(X + i, Y , Z + j, X + i, Y , Z + j, foundationBlockBorder)
                if i!= (size//2)-1 and i!= size//2 and i!= (size//2)+1 and j!= (size//2)-1 and j!= size//2 and j!= (size//2)+1: 
                    GEO.placeCuboid(X + i, Y + 1, Z + j, X + i, Y + 1, Z + j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
            else: GEO.placeCuboid(X + i, Y , Z + j, X + i, Y , Z + j, foundation)
    
    for i in range(-2,len(templateL)+2):
        for j in range(-2,len(templateL)+2):
            if i == -2 or j == -2 or i == size+1 or j == size+1:
                if i!= (size//2)-1 and i!= size//2 and i!= (size//2)+1 and j!= (size//2)-1 and j!= size//2 and j!= (size//2)+1: 
                    GEO.placeCuboid(X + i, Y + 1, Z + j, X + i, Y + 1, Z + j, "oak_fence"+"[north=true,south=true,east=true,west=true]")

    for h in range(0,14):
        for i in range(len(templateL)):
            for j in range(len(templateL[0])):
                if dir=="n":
                    m = templateL[i][j]
                elif dir=="s":
                    m = templateL[j][i]
                if h<=1:
                    if h == 0:
                        if m == 1 or m == 4 or m==7 or m == -2:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, mainBlock)
                        if m == -9:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "oak_leaves"+"[persistent=true]")
                        if m == -1:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "oak_planks")
                        if m == 9 or m == -5 or m == -6 or m == -7 or m == 5 or m == 6 or m == 8 or m == -20 or m== -21 or m==-31 or m == -32:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, carpets[r_carp])
                    elif h == 1:
                        if m == 1 or m == 4:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, mainBlock)
                        if m == 7 or m == -2:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "glass")
                        if m == -5:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "oak_planks")
                    if m == 2:
                        if dir=="n":
                            if h==1:GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h , Z+j, "oak_door"+"[facing=west,half=upper,hinge=right]")
                            else:GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h , Z+j, "oak_door"+"[facing=west,half=lower,hinge=right]")
                        else:
                            if h==1:GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h , Z+j, "oak_door"+"[facing=north,half=upper,hinge=left]")
                            else:GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h , Z+j, "oak_door"+"[facing=north,half=lower,hinge=left]")
                    if m == 3:
                        if dir=="n":
                            if h==1:GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h , Z+j, "oak_door"+"[facing=west,half=upper,hinge=left]")
                            else:GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h , Z+j, "oak_door"+"[facing=west,half=lower,hinge=left]")
                        else:
                            if h==1:GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h , Z+j, "oak_door"+"[facing=north,half=upper,hinge=right]")
                            else:GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h , Z+j, "oak_door"+"[facing=north,half=lower,hinge=right]")
                elif h == 2:
                    if m == 1 or  m == 2 or  m == 3 or m == 4:
                        GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, mainBlock)
                    if m == 7 or m == -2:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "glass")
                    if m == -6:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "oak_planks")
                elif h==3:
                    if m == 1 or  m == 2 or  m == 3 or m == 4 or m==7 or m == -2:
                        GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, mainBlock)
                    if m == -7:
                        GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "oak_planks")
                    if m == -20 or m== -21:
                        GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "lantern"+"[hanging=true]")

                # 2nd story
                elif h == 4 and (m == 9 or m == 8 or m == 1 or  m == 2 or  m == 3 or m == 4 or m == 5 or m == 6 or m==7 or m == -2 or m==0 or m == -20 or m== -21 or m==-31 or m == -32):
                    GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, accentBlock)
                elif h == 4 and (m == -11):
                    if dir=="n":
                        GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "spruce_stairs"+"[facing=west]")
                    else:
                        GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "spruce_stairs"+"[facing=north]")
                    GEO.placeCuboid(X+i, Y+1+h-1 , Z+j, X+i, Y+1+h-1, Z+j, "lantern"+"[hanging=true]")
                elif h == 4 and (m == -13):
                    GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, accentBlock)
                    GEO.placeCuboid(X+i, Y+1+h-1 , Z+j, X+i, Y+1+h-1, Z+j, "lantern"+"[hanging=true]")
                elif h == 5:
                    if m == 1 or m == 5 or  m == 2 or  m == 3 or m == 6 or m == -2:
                        GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, mainBlock)
                    if m == 9 or m== -20 or m== -21:
                        GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, carpets[r_carp])
                    
                    if dir =="n":
                        if m == -31:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, beds[r_bed]+"[part=head,facing=west]")
                        if m == -32:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, beds[r_bed]+"[part=foot,facing=west]")
                    else:
                        if m == -31:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, beds[r_bed]+"[part=head,facing=north]")
                        if m == -32:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, beds[r_bed]+"[part=foot,facing=north]")
                elif h == 5 or h == 6 or h == 7:
                    if m == 1 or m == 5 or  m == 2 or  m == 3:
                        GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, mainBlock)
                    if m == 6 or m == -2:
                        GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "glass")

                elif h == 8:
                    if m == 1 or m == 5 or  m == 2 or  m == 3 or m == 6 or m == -2:
                        GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, mainBlock)
                    if m == -20:
                        GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "lantern"+"[hanging=true]")

                elif h >= 9:
                    if m == 1 or m == 5 or  m == 2 or  m == 3 or m == 6 or m == 9 or m == -1 or m == -2 or m==-5 or m==-6 or m==-7 or m == -20 or m == -31 or m == -32:
                        GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, accentBlock)

    # types of shapes
    if dir == "s": # type 1
        roof = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
                [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
                [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
                [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
                [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
                [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
                [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
                [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
                [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

        h = 8
        c = 0
        for tx in range(len(roof[0])):
            for ty in range(len(roof)//2,len(roof)):
                v = roof[ty][tx]
                if v == 6:
                    GEO.placeCuboid(X+tx, Y+1+h+v, Z+ty, X+tx, Y+1+h+v, Z+ty, slab)
                else:
                    if c==0 or c==(len(roof[0]))-1:
                        GEO.placeCuboid(X+tx, Y+1+h+v, Z+ty, X+tx, Y+1+h+v, Z+ty, roofStairs2+"[facing=north]")
                    else:GEO.placeCuboid(X+tx, Y+1+h+v, Z+ty, X+tx, Y+1+h+v, Z+ty, roofStairs+"[facing=north]")
                    GEO.placeCuboid(X+tx, Y+1+h+v+1, Z+ty, X+tx, Y+1+h+v+1, Z+ty, "air")
                    GEO.placeCuboid(X+tx, Y+1+h+v+2, Z+ty, X+tx, Y+1+h+v+2, Z+ty, "air")
                    GEO.placeCuboid(X+tx, Y+1+h+v+3, Z+ty, X+tx, Y+1+h+v+3, Z+ty, "air")
            c+=1
        h = 8
        c=0
        for tx in range(len(roof[0])):
            for ty in range(0,len(roof)//2):
                v = roof[ty][tx]
                if c==0 or c==(len(roof[0]))-1:
                    GEO.placeCuboid(X+tx, Y+1+h+v, Z+ty, X+tx, Y+1+h+v, Z+ty, roofStairs2+"[facing=south]")
                else: GEO.placeCuboid(X+tx, Y+1+h+v, Z+ty, X+tx, Y+1+h+v, Z+ty, roofStairs+"[facing=south]")
                GEO.placeCuboid(X+tx, Y+1+h+v+1, Z+ty, X+tx, Y+1+h+v+1, Z+ty, "air")
                GEO.placeCuboid(X+tx, Y+1+h+v+2, Z+ty, X+tx, Y+1+h+v+2, Z+ty, "air")
                GEO.placeCuboid(X+tx, Y+1+h+v+3, Z+ty, X+tx, Y+1+h+v+3, Z+ty, "air")
            c+=1


        for i in range(0,len(templateL)):
            for j in range(0,len(templateL[0])):
                if templateL[j][i] == 8 or templateL[j][i] == -21:
                    GEO.placeCuboid(X+i, Y+6 , Z+j, X+i, Y+6, Z+j, "grass_block")
                    r = random.randint(0,len(flowers)-1)
                    GEO.placeCuboid(X+i, Y+7 , Z+j, X+i, Y+7, Z+j, flowers[r])
                if templateL[j][i] == 4 or templateL[j][i] == 7:
                    GEO.placeCuboid(X+i, Y+6 , Z+j, X+i, Y+6, Z+j, "oak_leaves"+"[persistent=true]")


    if dir == "n": # type 2
        roof = [[1,1,1,1,1,1,1,1,1,1,1],
                [2,2,2,2,2,2,2,2,2,2,2],
                [3,3,3,3,3,3,3,3,3,3,3],
                [4,4,4,4,4,4,4,4,4,4,4],
                [5,5,5,5,5,5,5,5,5,5,5],
                [6,6,6,6,6,6,6,6,6,6,6],
                [5,5,5,5,5,5,5,5,5,5,5],
                [4,4,4,4,4,4,4,4,4,4,4],
                [3,3,3,3,3,3,3,3,3,3,3],
                [2,2,2,2,2,2,2,2,2,2,2],
                [1,1,1,1,1,1,1,1,1,1,1]]

        h = 8
        for tx in range(len(roof[0])):
            for ty in range(len(roof)//2,len(roof)):
                v = roof[ty][tx]
                if v == 6:GEO.placeCuboid(X+tx, Y+1+h+v, Z+ty, X+tx, Y+1+h+v, Z+ty, slab)
                else:
                    GEO.placeCuboid(X+tx, Y+1+h+v, Z+ty, X+tx, Y+1+h+v, Z+ty, roofStairs+"[facing=north]")
                    GEO.placeCuboid(X+tx, Y+1+h+v+1, Z+ty, X+tx, Y+1+h+v+1, Z+ty, "air")
                    GEO.placeCuboid(X+tx, Y+1+h+v+2, Z+ty, X+tx, Y+1+h+v+2, Z+ty, "air")
                    GEO.placeCuboid(X+tx, Y+1+h+v+3, Z+ty, X+tx, Y+1+h+v+3, Z+ty, "air")
                    GEO.placeCuboid(X+tx, Y+1+h+v+4, Z+ty, X+tx, Y+1+h+v+4, Z+ty, "air")
                h = 8
        for tx in range(len(roof[0])):
            for ty in range(0,len(roof)//2):
                v = roof[ty][tx]
                GEO.placeCuboid(X+tx, Y+1+h+v, Z+ty, X+tx, Y+1+h+v, Z+ty, roofStairs+"[facing=south]")
                GEO.placeCuboid(X+tx, Y+1+h+v+1, Z+ty, X+tx, Y+1+h+v+1, Z+ty, "air")
                GEO.placeCuboid(X+tx, Y+1+h+v+2, Z+ty, X+tx, Y+1+h+v+2, Z+ty, "air")
                GEO.placeCuboid(X+tx, Y+1+h+v+3, Z+ty, X+tx, Y+1+h+v+3, Z+ty, "air")

        h = 10
        chim = [[1,1,1],
                [1,1,1]]
        for tx in range(len(chim[0])):
            for ty in range(len(chim)):
                for q in range(0,4):
                    GEO.placeCuboid(X+tx+8, Y+1+h+q, Z+ty+10, X+tx+8, Y+1+h+q, Z+ty+10, "air")
                    GEO.placeCuboid(X+tx+7, Y+1+h+q, Z+ty+10, X+tx+7, Y+1+h+q, Z+ty+10, "air")
                    GEO.placeCuboid(X+tx+6, Y+1+h+q, Z+ty+10, X+tx+6, Y+1+h+q, Z+ty+10, "air")
                    GEO.placeCuboid(X+tx+5, Y+1+h+q, Z+ty+10, X+tx+5, Y+1+h+q, Z+ty+10, "air")

                    GEO.placeCuboid(X+tx+4, Y+1+h+q, Z+ty+10, X+tx+4, Y+1+h+q, Z+ty+10, "air")
                    GEO.placeCuboid(X+tx+3, Y+1+h+q, Z+ty+10, X+tx+3, Y+1+h+q, Z+ty+10, "air")
                    GEO.placeCuboid(X+tx+2, Y+1+h+q, Z+ty+10, X+tx+2, Y+1+h+q, Z+ty+10, "air")
                    GEO.placeCuboid(X+tx+1, Y+1+h+q, Z+ty+10, X+tx+1, Y+1+h+q, Z+ty+10, "air")

                    GEO.placeCuboid(X+tx+8, Y+1+h+q, Z+ty+11, X+tx+8, Y+1+h+q, Z+ty+11, "air")
                    GEO.placeCuboid(X+tx+7, Y+1+h+q, Z+ty+11, X+tx+7, Y+1+h+q, Z+ty+11, "air")
                    GEO.placeCuboid(X+tx+6, Y+1+h+q, Z+ty+11, X+tx+6, Y+1+h+q, Z+ty+11, "air")
                    GEO.placeCuboid(X+tx+5, Y+1+h+q, Z+ty+11, X+tx+5, Y+1+h+q, Z+ty+11, "air")
                    GEO.placeCuboid(X+tx+4, Y+1+h+q, Z+ty+11, X+tx+4, Y+1+h+q, Z+ty+11, "air")
                    GEO.placeCuboid(X+tx+3, Y+1+h+q, Z+ty+11, X+tx+3, Y+1+h+q, Z+ty+11, "air")

                    GEO.placeCuboid(X+tx+8, Y+1+h+q, Z+ty+12, X+tx+8, Y+1+h+q, Z+ty+12, "air")
                    GEO.placeCuboid(X+tx+7, Y+1+h+q, Z+ty+12, X+tx+7, Y+1+h+q, Z+ty+12, "air")
                    GEO.placeCuboid(X+tx+6, Y+1+h+q, Z+ty+12, X+tx+6, Y+1+h+q, Z+ty+12, "air")
                    GEO.placeCuboid(X+tx+5, Y+1+h+q, Z+ty+12, X+tx+5, Y+1+h+q, Z+ty+12, "air")
                    GEO.placeCuboid(X+tx+4, Y+1+h+q, Z+ty+12, X+tx+4, Y+1+h+q, Z+ty+12, "air")
                    GEO.placeCuboid(X+tx+3, Y+1+h+q, Z+ty+12, X+tx+3, Y+1+h+q, Z+ty+12, "air")
        GEO.placeCuboid(X+1, Y+15 , Z+13, X+1, Y+15, Z+13, "campfire")
        GEO.placeCuboid(X+2, Y+15 , Z+13, X+2, Y+15, Z+13, "campfire")
        GEO.placeCuboid(X+1, Y+15 , Z+12, X+1, Y+15, Z+12, "campfire")
        GEO.placeCuboid(X+2, Y+15 , Z+12, X+2, Y+15, Z+12, "campfire")
        for i in range(0,len(templateL)):
            for j in range(0,len(templateL[0])):
                if templateL[i][j] == 8 or templateL[i][j] == -21:
                    GEO.placeCuboid(X+i, Y+6 , Z+j, X+i, Y+6, Z+j, "grass_block")
                    r = random.randint(0,len(flowers)-1)
                    GEO.placeCuboid(X+i, Y+7 , Z+j, X+i, Y+7, Z+j, flowers[r])
                if templateL[i][j] == 4 or templateL[i][j] == 7:
                    GEO.placeCuboid(X+i, Y+6 , Z+j, X+i, Y+6, Z+j, "oak_leaves"+"[persistent=true]")
    INTF.runCommand(f"summon villager {X+6} {Y+1} {Z+6}")
    
    if dir == "n":
        for h in range(0,14):
            for i in range(len(interiorL)):
                for j in range(len(interiorL[0])):
                    if dir=="n":
                        m = interiorL[i][j]
                    elif dir=="s":
                        m = interiorL[j][i]
                    if h == 0:
                        if m == 1:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, seats[r_seat]+"[facing=north]")
                        if m == 2:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, seats[r_seat]+"[facing=south]")
                        if m == 3:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "scaffolding")
                        
                        r1 = random.randint(1,7)
                        r2 = random.randint(1,7)
                        r3 = random.randint(1,7)
                        r4 = random.randint(1,7)
                        r5 = random.randint(1,7)
                        r6 = random.randint(1,7)
                        r7 = random.randint(1,7)
                        
                        if r1 ==1 or r2 ==1 or r3 ==1 or r4 ==1 or r5 ==1 or r6 ==1 or r7 ==1:
                            if m==4:
                                GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=south]")
                        if r1 ==2 or r2 ==2 or r3 ==2 or r4 ==2  or r5 ==2 or r6 ==2 or r7 ==2:
                            if m==5:
                                GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, itemsNodir[random.randint(0,len(itemsNodir)-1)])
                        if r1 ==3 or r2 ==3 or r3 ==3 or r4 ==3  or r5 ==3 or r6 ==3 or r7 ==3:
                            if m==6:
                                GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=east]")
                        if r1 ==4 or r2 ==4 or r3 ==4 or r4 ==4  or r5 ==4 or r6 ==4 or r7 ==4:
                            if m==7:
                                GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, itemsNodir[random.randint(0,len(itemsNodir)-1)])
                        if r1 ==5 or r2 ==5 or r3 ==5 or r4 ==5  or r5 ==5 or r6 ==5 or r7 ==5:
                            if m==8:
                                GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=north]")
                        if r1 ==6 or r2 ==6 or r3 ==6 or r4 ==6  or r5 ==6 or r6 ==6 or r7 ==6:
                            if m==9:
                                GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, itemsNodir[random.randint(0,len(itemsNodir)-1)])
                        if r1 ==7 or r2 ==7 or r3 ==7 or r4 ==7  or r5 ==7 or r6 ==7 or r7 ==7:
                            if m==10:
                                GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=west]")
                    if h == 5:
                        if m==5:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=east]")
                        if m==6:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=east]") 
                        if m==4:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=south]")
                        if m==5:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, itemsNodir[random.randint(0,len(itemsNodir)-1)])
                        if m==8:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=north]")
                        if m==10:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=west]")
                    if h == 2:
                        if m==11:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "lantern"+"[hanging=true]")
                    if h == 8:
                        if m==11:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "lantern"+"[hanging=true]")
                        if m==12:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "lantern"+"[hanging=true]")
    else:
        for h in range(0,14):
            for i in range(len(interiorL)):
                for j in range(len(interiorL[0])):
                    if dir=="n":
                        m = interiorL[i][j]
                    elif dir=="s":
                        m = interiorL[j][i]
                    if h == 0:
                        if m == 1:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, seats[r_seat]+"[facing=west]")
                        if m == 2:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, seats[r_seat]+"[facing=east]")
                        if m == 3:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "scaffolding") 
                        
                        r1 = random.randint(1,7)
                        r2 = random.randint(1,7)
                        r3 = random.randint(1,7)
                        r4 = random.randint(1,7)
                        r5 = random.randint(1,7)
                        r6 = random.randint(1,7)
                        r7 = random.randint(1,7)
                        if r1 ==1 or r2 ==1 or r3 ==1 or r3 ==1 or r4 ==1 or r5 ==1 or r6 ==1 or r7 ==1:
                            if m==4:
                                GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=east]")
                        if r1 ==2 or r2 ==2 or r3 ==2 or r3 ==2 or r4 ==2 or r5 ==2 or r6 ==2 or r7 ==2:
                            if m==5:
                                GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, itemsNodir[random.randint(0,len(itemsNodir)-1)])
                        if r1 ==3 or r2 ==3 or r3 ==3 or r3 ==3 or r4 ==3 or r5 ==3 or r6 ==3 or r7 ==3:
                            if m==6:
                                GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=south]")
                        if r1 ==4 or r2 ==4 or r3 ==4 or r3 ==4 or r4 ==4 or r5 ==4 or r6 ==4 or r7 ==4:
                            if m==7:
                                GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, itemsNodir[random.randint(0,len(itemsNodir)-1)])
                        if r1 ==5 or r2 ==5 or r3 ==5 or r3 ==5 or r4 ==5 or r5 ==5 or r6 ==5 or r7 ==5:
                            if m==8:
                                GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=west]")
                        if r1 ==6 or r2 ==6 or r3 ==6 or r3 ==6 or r4 ==6 or r5 ==6 or r6 ==6 or r7 ==6:
                            if m==9:
                                GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, itemsNodir[random.randint(0,len(itemsNodir)-1)])
                        if r1 ==7 or r2 ==7 or r3 ==7 or r3 ==7 or r4 ==7 or r5 ==7 or r6 ==7 or r7 ==7:
                            if m==10:
                                GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=north]")
                    if h == 5:
                        if m==5:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=south]")
                        if m==6:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=south]") 
                        if m==4:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=south]")
                        if m==5:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, itemsNodir[random.randint(0,len(itemsNodir)-1)])
                        if m==8:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=west]")
                        if m==10:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, items[random.randint(0,len(items)-1)]+"[facing=north]")
                    if h == 2:
                        if m==11:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "lantern"+"[hanging=true]")
                    if h == 8:
                        if m==11:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "lantern"+"[hanging=true]")
                        if m==12:
                            GEO.placeCuboid(X+i, Y+1+h , Z+j, X+i, Y+1+h, Z+j, "lantern"+"[hanging=true]")




