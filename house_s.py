from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL

import random
STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()

WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)
import numpy as np

def buildSqHouse(X, Y, Z,biome):
    X = X-(11//2)
    Z = Z-(11//2)
    # biome blocks
    if 'desert' in biome:
        foundation = "sandstone"
        foundationBlockBorder = "sandstone"
        roofBlock = "red_sandstone"
        roofStairs = "red_sandstone_stairs"
        slab = "red_sandstone_slab"
    elif 'ocean' in biome:
        foundation = "glass"
        foundationBlockBorder = "glass"
        roofBlock = "sea_lantern"
        roofStairs = "prismarine_brick_stairs"
        slab = "prismarine_brick_slab"
    elif 'forest' in biome:
        foundation = "infested_mossy_stone_bricks"
        foundationBlockBorder = "chiseled_stone_bricks"
        roofBlock = "spruce_planks"
        roofStairs = "spruce_stairs"
        slab = "dark_oak_slab"
    elif 'taiga' in biome:
        foundation = "stone_bricks"
        foundationBlockBorder = "chiseled_stone_bricks"
        roofBlock = "spruce_planks"
        roofStairs = "spruce_stairs"
        slab = "dark_oak_slab"
    elif 'snowy' in biome:
        foundation = "snow_block"
        foundationBlockBorder = "snow_block"
        roofBlock = "snow_block"
        roofStairs = "quartz_stairs"
        slab = "quartz_slab"
    
    r = random.randint(0,2)
    if r ==0: mainBlock = "acacia_planks"
    elif r ==1: mainBlock = "acacia_wood"
    elif r ==2: mainBlock = "birch_wood"

    # decorations
    itemsNodir = ["smithing_table","composter","cartography_table","fletching_table"]
    beds = ["blue_bed","cyan_bed","red_bed","white_bed","purple_bed","lime_bed","orange_bed"]
    items = ["chest","ender_chest","smoker","furnace"]
    carpets = ["blue_carpet","cyan_carpet","red_carpet","white_carpet","purple_carpet","lime_carpet","orange_carpet"]

    r_bed = random.randint(0,len(beds)-1)
    r_carp = random.randint(0,len(carpets)-1)

    size = random.randint(9,13)

    r1 = random.randint(0,100)
    if r1 <50: dir = "n"
    else: dir = "s"

    # layout grid layer by layer
    layer_1 = np.zeros((size,size))
    for i in range(1,size-1):
        for j in range(1,size-1):
            layer_1[i][j] = 1
    for i in range(2,size-2):
        for j in range(2,size-2):
            r2 = random.randint(0,2)
            if r2==0:
                layer_1[i][j] = 11
            if r2==1:
                layer_1[i][j] = 12
            if r2==2:
                layer_1[i][j] = 0
    for i in range(3,size-3):
        for j in range(3,size-3):
            layer_1[i][j] = -1

    

    layer_2 = layer_1.copy()
    layer_2[1][(size//2)-1] = 2
    layer_2[1][size//2] = 2
    layer_2[1][(size//2)+1] = 2
    layer_2[size-2][(size//2)-1] = 2
    layer_2[size-2][size//2] = 2
    layer_2[size-2][(size//2)+1] = 2

    layer_2[(size//2)-1][1] = 2
    layer_2[(size//2)][1] = 2
    layer_2[(size//2)+1][1] = 2

    layer_1[size//2][size-2] = 4
    layer_1[(size//2)-1][size-2] = 3
    layer_1[size//2][size-3] = 0
    layer_1[(size//2)-1][size-3] = 0
    layer_1[(size//2)-1][size//2] = 21
    layer_1[(size//2)-1][(size//2)-1] = 22
    layer_2[size//2][size-2] = 0
    layer_2[(size//2)-1][size-2] = 0

    layer_4 = np.zeros((size,size))
    for i in range(1,size-1):
        for j in range(1,size-1):
            layer_4[i][j] = 1
    for i in range(2,size-2):
        for j in range(2,size-2): 
            layer_4[i][j] = 0

    layer_4[(size//2)][2] = 2
    layer_4[2][size//2] = 2
    layer_4[size-3][size//2] = 2

    layer_3 = layer_2.copy()
    layer_3[size//2][size-2] = 1
    layer_3[(size//2)-1][size-2] = 1
    

    layer_5 = np.zeros((size,size))
    for i in range(1,size-1):
        for j in range(1,size-1):
            layer_5[i][j] = 1

    # Place blocks

    for i in range(-2,size+2):
        for j in range(-2,size+2):
            if i == -2 or j == -2 or i == size+1 or j == size+1:
                GEO.placeCuboid(X + i, Y , Z + j, X + i, Y , Z + j, foundationBlockBorder)
                if i!= (size//2)-1 and i!= size//2 and i!= (size//2)+1 and j!= (size//2)-1 and j!= size//2 and j!= (size//2)+1: 
                    GEO.placeCuboid(X + i, Y + 1, Z + j, X + i, Y + 1, Z + j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
            else: GEO.placeCuboid(X + i, Y , Z + j, X + i, Y , Z + j, foundation)
    for i in range(-2,size+2):
        for j in range(-2,size+2):
            if i == -2 or j == -2 or i == size+1 or j == size+1:
                if i!= (size//2)-1 and i!= size//2 and i!= (size//2)+1 and j!= (size//2)-1 and j!= size//2 and j!= (size//2)+1: 
                    GEO.placeCuboid(X + i, Y + 1, Z + j, X + i, Y + 1, Z + j, "oak_fence"+"[north=true,south=true,east=true,west=true]")

    Y+=1

    for i in range(0,size):
        for j in range(0,size):
            if dir=="s":
                a = layer_1[i][j]
            elif dir=="n":
                a = layer_1[j][i]
            if a == 1:
                GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, mainBlock)
            elif a == 3:
                if dir=="n":
                    GEO.placeCuboid(X + i, Y + 1, Z + j, X + i, Y + 1, Z + j, "oak_door" + "[facing=west,half=upper,hinge=right]")
                    GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, "oak_door" + "[facing=west,half=lower,hinge=right]")
                    GEO.placeCuboid(X + i +1 , Y, Z + j -1 , X + i+1, Y, Z + j - 1, "oak_leaves"+"[persistent=true]")
                    GEO.placeCuboid(X + i +1 , Y, Z + j + 2, X + i+1, Y, Z + j + 2, "oak_leaves"+"[persistent=true]")
                else:
                    GEO.placeCuboid(X + i, Y + 1, Z + j, X + i, Y + 1, Z + j, "oak_door" + "[facing=north,half=upper,hinge=left]")
                    GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, "oak_door" + "[facing=north,half=lower,hinge=left]")
                    GEO.placeCuboid(X + i -1 , Y, Z + j +1, X + i -1, Y, Z + j +1, "oak_leaves"+"[persistent=true]")
                    GEO.placeCuboid(X + i +2, Y, Z + j +1, X + i +2, Y, Z + j +1, "oak_leaves"+"[persistent=true]")
            elif a == 4:
                GEO.placeCuboid(X + i, Y + 1, Z + j, X + i, Y + 1, Z + j, "oak_door" + "[facing=north,half=upper,hinge=right]")
                GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, "oak_door" + "[facing=north,half=lower,hinge=right]")
            elif a == 11:
                GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, itemsNodir[random.randint(0,len(itemsNodir)-1)])
            elif a == 12:
                GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, items[random.randint(0,len(items)-1)])
            elif a == 21:
                if dir=="s":
                    GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, beds[r_bed]+"[part=foot]")
                if dir=="n":
                    GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, beds[r_bed]+"[part=foot,facing=west]")
            elif a == 22:
                if dir=="s":
                    GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, beds[r_bed]+"[part=head]")
                if dir=="n":
                    GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, beds[r_bed]+"[part=head,facing=west]")
            elif a == -1:
                GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, carpets[r_carp])

    Y+=1
    for i in range(0,size):
        for j in range(0,size):
            if dir=="s":
                a = layer_2[i][j]
            elif dir=="n":
                a = layer_2[j][i]
            if a==1:
                GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, mainBlock)
            elif a==2:
                GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, "glass")
    Y+=1
    for i in range(0,size):
        for j in range(0,size):
            if dir=="s":
                a = layer_3[i][j]
            elif dir=="n":
                a = layer_3[j][i]
            if a==1:
                GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, mainBlock)
            elif a==2:
                GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, "glass")
                
    Y+=1
    for i in range(0,size):
        for j in range(0,size):
            if dir=="s":
                a = layer_4[i][j]
            elif dir=="n":
                a = layer_4[j][i]
            if a>0:
                GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, mainBlock)
                if a==2:
                    GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, "lantern"+"[hanging=true]")
    Y+=1
    for i in range(0,size):
        for j in range(0,size):
            if dir=="s":
                a = layer_5[i][j]
            elif dir=="n":
                a = layer_5[j][i]
            if a>0:
                GEO.placeCuboid(X + i, Y, Z + j, X + i, Y, Z + j, mainBlock)
    INTF.runCommand(f"summon villager {X+3} {Y} {Z+3}")


    roofR = random.randint(0,100)
    if roofR < 50:
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
        roof[size//2][size//2] = roof[(size//2)-1][size//2] -1
        h = 0
        for tx in range(0,len(roof[0])):
            for ty in range(0,len(roof)):
                v = int(roof[ty][tx])
                if (tx == 0 and ty == 0) or (tx == 0 and ty == size-1) or (tx == size-1 and ty == 0) or (tx == size-1 and ty == size-1):
                    GEO.placeCuboid(X+tx, Y, Z+ty, X+tx, Y, Z+ty,"lantern"+"[hanging=true]")
                GEO.placeCuboid(X + tx, Y + 1 + h + v, Z + ty, X + tx, Y + 1 + h + v, Z + ty, roofBlock)
                if tx == size//2 and ty == size//2:
                    GEO.placeCuboid(X + tx, Y + 1 + h + v, Z + ty, X + tx, Y + 1 + h + v, Z + ty, "campfire")

    else:
        roof = np.zeros((size,size))
        for rx in range(0,size//2):
            for ry in range(0,size):
                roof[rx][ry] = rx+1
        for rx in range(size//2,size):
            for ry in range(0,size):
                roof[rx][ry] = size - rx
        
        h = 0
        for tx in range(size):
            for ty in range(size):
                if (tx == 0 and ty == 0) or (tx == 0 and ty == size-1) or (tx == size-1 and ty == 0) or (tx == size-1 and ty == size-1):
                    GEO.placeCuboid(X+tx, Y-1, Z+ty, X+tx, Y-1, Z+ty,"lantern"+"[hanging=true]")
                GEO.placeCuboid(X+tx, Y+1+h, Z+ty, X+tx, Y+1+h, Z+ty, "spruce_planks")
                GEO.placeCuboid(X+tx, Y+1+h+1, Z+ty, X+tx, Y+1+h+1, Z+ty, "spruce_planks")
                GEO.placeCuboid(X+tx, Y+1+h+2, Z+ty, X+tx, Y+1+h+2, Z+ty, "spruce_planks")
                GEO.placeCuboid(X+tx, Y+1+h+3, Z+ty, X+tx, Y+1+h+3, Z+ty, "spruce_planks")

                

        h = -2
        for tx in range(len(roof[0])):
            for ty in range(len(roof)//2,len(roof)):
                v = (int)(roof[ty][tx])
                if v == 6:GEO.placeCuboid(X+tx, Y+1+h+v, Z+ty, X+tx, Y+1+h+v, Z+ty, slab)
                else:
                    GEO.placeCuboid(X+tx, Y+1+h+v, Z+ty, X+tx, Y+1+h+v, Z+ty, roofStairs+"[facing=north]")
                    GEO.placeCuboid(X+tx, Y+1+h+v+1, Z+ty, X+tx, Y+1+h+v+1, Z+ty, "air")
                    GEO.placeCuboid(X+tx, Y+1+h+v+2, Z+ty, X+tx, Y+1+h+v+2, Z+ty, "air")
                    GEO.placeCuboid(X+tx, Y+1+h+v+3, Z+ty, X+tx, Y+1+h+v+3, Z+ty, "air")
                    GEO.placeCuboid(X+tx, Y+1+h+v+4, Z+ty, X+tx, Y+1+h+v+4, Z+ty, "air")
        h = -2
        for tx in range(len(roof[0])):
            for ty in range(0,len(roof)//2):
                v = (int)(roof[ty][tx])
                GEO.placeCuboid(X+tx, Y+1+h+v, Z+ty, X+tx, Y+1+h+v, Z+ty, roofStairs+"[facing=south]")
                GEO.placeCuboid(X+tx, Y+1+h+v+1, Z+ty, X+tx, Y+1+h+v+1, Z+ty, "air")
                GEO.placeCuboid(X+tx, Y+1+h+v+2, Z+ty, X+tx, Y+1+h+v+2, Z+ty, "air")
                GEO.placeCuboid(X+tx, Y+1+h+v+3, Z+ty, X+tx, Y+1+h+v+3, Z+ty, "air")
                GEO.placeCuboid(X+tx, Y+1+h+v+4, Z+ty, X+tx, Y+1+h+v+4, Z+ty, "air")
