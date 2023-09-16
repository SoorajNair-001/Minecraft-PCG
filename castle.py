from gdpc import interfaceUtils as INTF
from gdpc import geometry as GEO
import random
import numpy as np

import matplotlib as mpl
from matplotlib import pyplot


def buildCastle(x,y,z,biome):
    foundation(x,y,z,biome)
    structure(x,y,z,biome)
    cartRide(x+3,y+3,z-5)


def structure(x,y,z,biome):
    # biome blocks
    if 'desert' in biome:
        mainBlock = "chiseled_sandstone"
        accentBlock = "chiseled_red_sandstone"
    elif 'ocean' in biome:
        mainBlock = "prismarine_bricks"
        accentBlock = "sea_lantern"
    elif 'forest' in biome:
        mainBlock = "infested_mossy_stone_bricks"
        accentBlock = "stripped_birch_wood"
    elif 'taiga' in biome:
        mainBlock = "infested_mossy_stone_bricks"
        accentBlock = "stripped_birch_wood"
    elif 'snowy' in biome:
        mainBlock = "snow_block"
        accentBlock = "packed_ice"


    # making layout map
    size = 40
    X = x-(size//2)
    Z = z-(size//2)
    layout = np.zeros((size,size))
    for i in range(3,size-3):
        for j in range(3,size-3):
            layout[i][j] = 1
    for i in range(4,size-4):
        for j in range(4,size-4):
            layout[i][j] = 0
    
    a = 1
    for i in range(a,a+9):
        for j in range(a,a+9):
            layout[i][j] = 0
            layout[i+29][j] = 0
            layout[i][j+29] = 0
            layout[i+29][j+29] = 0

    layout[6][6] = 2
    layout[6][size-7] = 2
    layout[size-7][6] = 2
    layout[size-7][size-7] = 2

    layout[3][(size//2)-3] = 3
    layout[3][(size//2)-2] = 4
    layout[3][(size//2)-1] = 4
    layout[3][size//2] = 3
    layout[3][(size//2)+1] = 4
    layout[3][(size//2)+2] = 4
    layout[3][(size//2)+3] = 3
    
    layout[size-4][(size//2)-3] = 3
    layout[size-4][(size//2)-2] = 4
    layout[size-4][(size//2)-1] = 4
    layout[size-4][size//2] = 3
    layout[size-4][(size//2)+1] = 4
    layout[size-4][(size//2)+2] = 4
    layout[size-4][(size//2)+3] = 3

    layout[(size//2)-3][3] = 3
    layout[(size//2)-2][3] = 4
    layout[(size//2)-1][3] = 4
    layout[(size//2)][3] = 3
    layout[(size//2)+1][3] = 4
    layout[(size//2)+2][3] = 4
    layout[(size//2)+3][3] = 3

    layout[(size//2)-3][size-4] = 3
    layout[(size//2)-2][size-4] = 4
    layout[(size//2)-1][size-4] = 4
    layout[(size//2)][size-4] = 3
    layout[(size//2)+1][size-4] = 4
    layout[(size//2)+2][size-4] = 4
    layout[(size//2)+3][size-4] = 3

    # placing the blocks
    for i in range(0,size):
        for j in range(0,size):
            if layout[i][j] == 1 or layout[i][j] == 3 or layout[i][j] == 4:
                for yy in range(0,21):
                    INTF.setBlock(X + i, y+yy, Z + j, mainBlock)
    for i in range(0,size):
        for j in range(0,size):
            if layout[i][j] == 3 or layout[i][j] == 4:
                if layout[i][j] == 4:
                    INTF.setBlock(X + i, y+3, Z + j, "jungle_door"+"[half=lower]")
                    INTF.setBlock(X + i, y+4, Z + j, "jungle_door"+"[half=upper]")
                else:
                    INTF.setBlock(X + i, y+3, Z + j, accentBlock)
                    INTF.setBlock(X + i, y+4, Z + j, accentBlock)
                INTF.setBlock(X + i, y+5, Z + j, accentBlock)
                INTF.setBlock(X + i, y+6, Z + j, accentBlock)
                INTF.setBlock(X + i, y+7, Z + j, accentBlock)
                INTF.setBlock(X + i, y+8, Z + j, accentBlock)

    for yy in range(0,5):
        for i in range(3-yy,size-3+yy):
            for j in range(3-yy,size-3+yy):
                GEO.placeCuboid(X + i, y+20+yy, Z + j,X + i, y+20+yy, Z + j, mainBlock)
        if yy ==4:
            for i in range(10,size-10):
                for j in range(10,size-10):
                    GEO.placeCuboid(X + i, y+20+yy, Z + j,X + i, y+20+yy, Z + j, "glass")
            for i in range(17,size-17):
                for j in range(17,size-17):
                    GEO.placeCuboid(X + i, y+20+yy, Z + j,X + i, y+20+yy, Z + j, "air")
            for i in range(16,size-16):
                for j in range(16,size-16):
                    if i==16 or i==size-17 or j==16 or j==size-17:
                        GEO.placeCuboid(X + i, y+20+yy+1, Z + j,X + i, y+20+yy+1, Z + j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
            for i in range(16,size-16):
                for j in range(16,size-16):
                    if i==16 or i==size-17 or j==16 or j==size-17:
                        GEO.placeCuboid(X + i, y+20+yy+1, Z + j,X + i, y+20+yy+1, Z + j, "oak_fence"+"[north=true,south=true,east=true,west=true]")
        else:
            for i in range(10,size-10):
                for j in range(10,size-10):
                    GEO.placeCuboid(X + i, y+20+yy, Z + j,X + i, y+20+yy, Z + j, "air")
    
    for i in range(0,size):
            for j in range(0,size):
                if i==0 or i==size-1 or j==0 or j==size-1:
                    INTF.setBlock(X + i, y+20+5, Z + j, accentBlock)
                    
    
    for i in range(0,size):
        for j in range(0,size):
            if layout[i][j] == 2:
                GEO.placeCylinder(X + i -6,y,Z + j-6,X + i +6,y+20,Z + j +6,accentBlock,replace=True,
                  axis='y', tube=False, hollow=True)
                for xx in range(-1,2):
                    for yy in range(-1,2):
                        INTF.setBlock(X + i +xx,y+1,Z + j+yy,"emerald_block")
                        INTF.setBlock(X + i +xx,y+2,Z + j+yy,"air")
                        INTF.setBlock(X + i +xx,y+3,Z + j+yy,"air")
                        INTF.setBlock(X + i +xx,y+4,Z + j+yy,"air")
                        INTF.setBlock(X + i +xx,y+5,Z + j+yy,"air")
                        INTF.setBlock(X + i +xx,y+20,Z + j+yy,"air")
                        INTF.setBlock(X + i +xx,y+21,Z + j+yy,"air")
                        INTF.setBlock(X + i +xx,y+22,Z + j+yy,"air")
                        INTF.setBlock(X + i +xx,y+23,Z + j+yy,"air")
                        INTF.setBlock(X + i +xx,y+24,Z + j+yy,"glass")
                INTF.setBlock(X + i,y+2,Z + j,"beacon")

                for yy in range(2,19):
                    INTF.setBlock(X + i +6,y+yy,Z + j,"glass")
                    INTF.setBlock(X + i,y+yy,Z + j +6,"glass")
                    INTF.setBlock(X + i -6,y+yy,Z + j,"glass")
                    INTF.setBlock(X + i,y+yy,Z + j-6,"glass")



# minecrat elevator ride
def cartRide(x,y,z):

    base = "chiseled_stone_bricks"
    ry = y
    INTF.setBlock(x -5 , ry-1, z, base)
    INTF.setBlock(x -5 , ry, z, "powered_rail")
    INTF.setBlock(x -6 , ry-1, z, base)
    INTF.setBlock(x -6 , ry, z, "powered_rail")
    INTF.setBlock(x -7 , ry-1, z, base)
    INTF.setBlock(x -7 , ry, z, "rail")
    INTF.setBlock(x -8 , ry-1, z, base)
    INTF.setBlock(x -8 , ry, z, "powered_rail")
    INTF.runCommand(f"summon minecart {x -8} {ry+1} {z}")
    INTF.setBlock(x -9 , ry-1, z, base)
    INTF.setBlock(x -9 , ry, z, base)
    INTF.setBlock(x -9 , ry+1, z, "spruce_button"+"[face=floor,facing=north]")
    for i in range(-4,4):
        if i==3:
            ry -= 1
            INTF.setBlock(x + i, ry, z, base)
            INTF.setBlock(x + i, ry+1, z, "rail")
        else:
            if i==0:
                INTF.setBlock(x + i, ry, z-1, base)
                INTF.setBlock(x + i, ry+1, z-1, "redstone_torch"+"[lit=true]")
            INTF.setBlock(x + i, ry, z, base)
            INTF.setBlock(x + i, ry+1, z, "powered_rail")
        ry += 1
    ry -= 1
    for j in range(1,8):
        if i==7:
            ry -= 1
            INTF.setBlock(x + 3, ry, z + j, base)
            INTF.setBlock(x + 3, ry+1, z + j, "powered_rail")
        else:
            if j==5:
                INTF.setBlock(x + 4, ry, z + j, base)
                INTF.setBlock(x + 4, ry+1, z + j, "redstone_torch"+"[lit=true]")
            INTF.setBlock(x + 3, ry, z + j, base)
            INTF.setBlock(x + 3, ry+1, z + j, "powered_rail")
        ry += 1
    ry -= 2
    for i in range(-3,5):
        if i==4:
            ry -= 1
        if i == -3:
            INTF.setBlock(x - i, ry+1, z + 8, base)
            INTF.setBlock(x - i, ry+2, z + 8, "rail")
        elif i == 4:
            INTF.setBlock(x - i, ry, z + 8, base)
            INTF.setBlock(x - i, ry+1, z + 8, "rail")
        else:
            if i == 1:
                INTF.setBlock(x - i, ry, z + 9, base)
                INTF.setBlock(x - i, ry+1, z + 9, "redstone_torch"+"[lit=true]")
            INTF.setBlock(x - i, ry, z + 8, base)
            INTF.setBlock(x - i, ry+1, z + 8, "powered_rail")
        ry += 1
    ry -= 1
    for j in range(-7,-1):
        if i==1:
            ry -= 1
            INTF.setBlock(x - 4, ry, z - j, base)
            INTF.setBlock(x - 4, ry+1, z - j, "rail")
        else:
            if j==-3:
                INTF.setBlock(x - 5, ry, z - j, base)
                INTF.setBlock(x - 5, ry+1, z - j, "redstone_torch"+"[lit=true]")
            INTF.setBlock(x - 4, ry, z - j, base)
            INTF.setBlock(x - 4, ry+1, z - j, "powered_rail")
        ry += 1
    INTF.setBlock(x - 4, ry-1, z + 1, base)
    INTF.setBlock(x - 4, ry, z + 1, "powered_rail")
    INTF.setBlock(x - 4, ry-1, z - 0, base)
    INTF.setBlock(x - 4, ry, z - 0, "powered_rail")
    INTF.setBlock(x - 4, ry-1, z - 1, base)
    INTF.setBlock(x - 4, ry, z - 1, "rail")
    INTF.setBlock(x - 4, ry-1, z - 2, base)
    INTF.setBlock(x - 4, ry, z - 2, "powered_rail")
    INTF.runCommand(f"summon minecart {x - 4} {ry+1} {z - 2}")
    INTF.setBlock(x - 4, ry-1, z - 3, base)
    INTF.setBlock(x - 4, ry, z - 3, base)
    INTF.setBlock(x - 4, ry+1, z - 3, "spruce_button" +"[face=floor,facing=north]")

# castle foundation
def foundation(x,y,z,biome):
    if 'desert' in biome:
        biomeBlock = "sandstone"
    elif 'ocean' in biome:
        biomeBlock = "prismarine_bricks"
    elif 'forest' in biome:
        biomeBlock = "infested_mossy_stone_bricks"
    elif 'taiga' in biome:
        biomeBlock = "infested_mossy_stone_bricks"
    elif 'snowy' in biome:
        biomeBlock = "snow_block"
    
    mainBlock = "chiseled_stone_bricks"
    slab1 = "stone_brick_slab"
    slab2 = "stone_slab"
    accentBlock = "polished_andesite"
    stairBlocks = "polished_andesite_stairs"
    lanternBlock = "lantern"
    print("Building castle foundation...")
    for i in range(-24,24):
        for j in range(-24,24):
            GEO.placeCuboid(x+i, y, z+j, x+i, y + 25, z+j, "air")

    for i in range(-26,27):
        for j in range(-5,5):
            GEO.placeCuboid(x+i, y, z+j, x+i, y + 10, z+j, "air")
    for i in range(-5,5):
        for j in range(-26,27):
            GEO.placeCuboid(x+i, y, z+j, x+i, y + 10, z+j, "air")

    for yy in range(3):
        for xx in range(27):
            for zz in range(47):
                INTF.placeBlockBatched(x - 13 + xx, y + yy, z - 23 + zz, biomeBlock)
        for xx in range(10):
            for zz in range(27):
                INTF.placeBlockBatched(x - 14 - xx, y + yy, z - 13 + zz, biomeBlock)
                INTF.placeBlockBatched(x + 14 + xx, y + yy, z - 13 + zz, biomeBlock)

    # Placing blocks
    INTF.placeBlockBatched(x + 4, y + 3, z - 23, mainBlock)
    INTF.placeBlockBatched(x + 9, y + 3, z - 23, mainBlock)
    INTF.placeBlockBatched(x + 13, y + 3, z - 23, mainBlock)

    INTF.placeBlockBatched(x - 4, y + 3, z - 23, mainBlock)
    INTF.placeBlockBatched(x - 9, y + 3, z - 23, mainBlock)
    INTF.placeBlockBatched(x - 13, y + 3, z - 23, mainBlock)

    INTF.placeBlockBatched(x + 4, y + 4, z - 23, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x + 9, y + 4, z - 23, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x + 13, y + 4, z - 23, slab1 + "[type=bottom]")

    INTF.placeBlockBatched(x - 4, y + 4, z - 23, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x - 9, y + 4, z - 23, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x - 13, y + 4, z - 23, slab1 + "[type=bottom]")

    INTF.placeBlockBatched(x + 4, y + 3, z + 23, mainBlock)
    INTF.placeBlockBatched(x + 9, y + 3, z + 23, mainBlock)
    INTF.placeBlockBatched(x + 13, y + 3, z + 23, mainBlock)

    INTF.placeBlockBatched(x - 4, y + 3, z + 23, mainBlock)
    INTF.placeBlockBatched(x - 9, y + 3, z + 23, mainBlock)
    INTF.placeBlockBatched(x - 13, y + 3, z + 23, mainBlock)

    INTF.placeBlockBatched(x + 4, y + 4, z + 23, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x + 9, y + 4, z + 23, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x + 13, y + 4, z + 23, slab1 + "[type=bottom]")

    INTF.placeBlockBatched(x - 4, y + 4, z + 23, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x - 9, y + 4, z + 23, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x - 13, y + 4, z + 23, slab1 + "[type=bottom]")

    for xx in range(4):
        INTF.placeBlockBatched(x + 5 + xx, y + 3, z - 23, slab2 + "[type=top]")
        INTF.placeBlockBatched(x - 5 - xx, y + 3, z - 23, slab2 + "[type=top]")
        INTF.placeBlockBatched(x + 5 + xx, y + 3, z + 23, slab2 + "[type=top]")
        INTF.placeBlockBatched(x - 5 - xx, y + 3, z + 23, slab2 + "[type=top]")
    for xx in range(3):
        INTF.placeBlockBatched(x + 10 + xx, y + 3, z - 23, slab2 + "[type=top]")
        INTF.placeBlockBatched(x - 10 - xx, y + 3, z - 23, slab2 + "[type=top]")
        INTF.placeBlockBatched(x + 10 + xx, y + 3, z + 23, slab2 + "[type=top]")
        INTF.placeBlockBatched(x - 10 - xx, y + 3, z + 23, slab2 + "[type=top]")
    
    INTF.placeBlockBatched(x - 23, y + 3, z + 4, mainBlock)
    INTF.placeBlockBatched(x - 23, y + 3, z + 9, mainBlock)
    INTF.placeBlockBatched(x - 23, y + 3, z + 13, mainBlock)

    INTF.placeBlockBatched(x - 23, y + 3, z - 4, mainBlock)
    INTF.placeBlockBatched(x - 23, y + 3, z - 9, mainBlock)
    INTF.placeBlockBatched(x - 23, y + 3, z - 13, mainBlock)

    INTF.placeBlockBatched(x - 23, y + 4, z + 4, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x - 23, y + 4, z + 9, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x - 23, y + 4, z + 13, slab1 + "[type=bottom]")

    INTF.placeBlockBatched(x - 23, y + 4, z - 4, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x - 23, y + 4, z - 9, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x - 23, y + 4, z - 13, slab1 + "[type=bottom]")
    
    INTF.placeBlockBatched(x + 23, y + 3, z + 4, mainBlock)
    INTF.placeBlockBatched(x + 23, y + 3, z + 9, mainBlock)
    INTF.placeBlockBatched(x + 23, y + 3, z + 13, mainBlock)

    INTF.placeBlockBatched(x + 23, y + 3, z - 4, mainBlock)
    INTF.placeBlockBatched(x + 23, y + 3, z - 9, mainBlock)
    INTF.placeBlockBatched(x + 23, y + 3, z - 13, mainBlock)

    INTF.placeBlockBatched(x + 23, y + 4, z + 4, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x + 23, y + 4, z + 9, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x + 23, y + 4, z + 13, slab1 + "[type=bottom]")

    INTF.placeBlockBatched(x + 23, y + 4, z - 4, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x + 23, y + 4, z - 9, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x + 23, y + 4, z - 13, slab1 + "[type=bottom]")


    for zz in range(4):
        INTF.placeBlockBatched(x - 23, y + 3, z + 5 + zz, slab2 + "[type=top]")
        INTF.placeBlockBatched(x - 23, y + 3, z - 5 - zz, slab2 + "[type=top]")
        INTF.placeBlockBatched(x + 23, y + 3, z + 5 + zz, slab2 + "[type=top]")
        INTF.placeBlockBatched(x + 23, y + 3, z + -5 - zz, slab2 + "[type=top]")
    for zz in range(3):
        INTF.placeBlockBatched(x + 23, y + 3, z + 10 + zz, slab2 + "[type=top]")
        INTF.placeBlockBatched(x + 23, y + 3, z - 10 - zz, slab2 + "[type=top]")
        INTF.placeBlockBatched(x - 23, y + 3, z + 10 + zz, slab2 + "[type=top]")
        INTF.placeBlockBatched(x - 23, y + 3, z - 10 - zz, slab2 + "[type=top]")

    INTF.placeBlockBatched(x - 13, y + 3, z - 13, mainBlock)
    INTF.placeBlockBatched(x - 13, y + 4, z - 13, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x - 18, y + 3, z - 13, mainBlock)
    INTF.placeBlockBatched(x - 18, y + 4, z - 13, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x - 13, y + 3, z - 18, mainBlock)
    INTF.placeBlockBatched(x - 13, y + 4, z - 18, slab1 + "[type=bottom]")

    INTF.placeBlockBatched(x + 13, y + 3, z - 13, mainBlock)
    INTF.placeBlockBatched(x + 13, y + 4, z - 13, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x + 18, y + 3, z - 13, mainBlock)
    INTF.placeBlockBatched(x + 18, y + 4, z - 13, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x + 13, y + 3, z - 18, mainBlock)
    INTF.placeBlockBatched(x + 13, y + 4, z - 18, slab1 + "[type=bottom]")

    INTF.placeBlockBatched(x - 13, y + 3, z + 13, mainBlock)
    INTF.placeBlockBatched(x - 13, y + 4, z + 13, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x - 18, y + 3, z + 13, mainBlock)
    INTF.placeBlockBatched(x - 18, y + 4, z + 13, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x - 13, y + 3, z + 18, mainBlock)
    INTF.placeBlockBatched(x - 13, y + 4, z + 18, slab1 + "[type=bottom]")

    INTF.placeBlockBatched(x + 13, y + 3, z + 13, mainBlock)
    INTF.placeBlockBatched(x + 13, y + 4, z + 13, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x + 18, y + 3, z + 13, mainBlock)
    INTF.placeBlockBatched(x + 18, y + 4, z + 13, slab1 + "[type=bottom]")
    INTF.placeBlockBatched(x + 13, y + 3, z + 18, mainBlock)
    INTF.placeBlockBatched(x + 13, y + 4, z + 18, slab1 + "[type=bottom]")

    for xx in range(4):
        INTF.placeBlockBatched(x - 14 - xx, y + 3, z - 13, slab2 + "[type=top]")
        INTF.placeBlockBatched(x - 19 - xx, y + 3, z - 13, slab2 + "[type=top]")
        INTF.placeBlockBatched(x - 14 - xx, y + 3, z + 13, slab2 + "[type=top]")
        INTF.placeBlockBatched(x - 19 - xx, y + 3, z + 13, slab2 + "[type=top]")
        INTF.placeBlockBatched(x + 14 + xx, y + 3, z - 13, slab2 + "[type=top]")
        INTF.placeBlockBatched(x + 19 + xx, y + 3, z - 13, slab2 + "[type=top]")
        INTF.placeBlockBatched(x + 14 + xx, y + 3, z + 13, slab2 + "[type=top]")
        INTF.placeBlockBatched(x + 19 + xx, y + 3, z + 13, slab2 + "[type=top]")

        INTF.placeBlockBatched(x - 5 - xx, y + 2, z + 19, mainBlock)
        INTF.placeBlockBatched(x - 5 - xx, y + 2, z - 19, mainBlock)
        INTF.placeBlockBatched(x + 5 + xx, y + 2, z + 19, mainBlock)
        INTF.placeBlockBatched(x + 5 + xx, y + 2, z - 19, mainBlock)
        INTF.placeBlockBatched(x + 10 + xx, y + 2, z + 9, mainBlock)
        INTF.placeBlockBatched(x + 15 + xx, y + 2, z + 9, mainBlock)
        INTF.placeBlockBatched(x - 10 - xx, y + 2, z + 9, mainBlock)
        INTF.placeBlockBatched(x - 15 - xx, y + 2, z + 9, mainBlock)
        INTF.placeBlockBatched(x + 10 + xx, y + 2, z - 9, mainBlock)
        INTF.placeBlockBatched(x + 15 + xx, y + 2, z - 9, mainBlock)
        INTF.placeBlockBatched(x - 10 - xx, y + 2, z - 9, mainBlock)
        INTF.placeBlockBatched(x - 15 - xx, y + 2, z - 9, mainBlock)
    for zz in range(4):
        INTF.placeBlockBatched(x - 13, y + 3, z - 14 - zz, slab2 + "[type=top]")
        INTF.placeBlockBatched(x - 13, y + 3, z - 19 - zz, slab2 + "[type=top]")
        INTF.placeBlockBatched(x - 13, y + 3, z + 14 + zz, slab2 + "[type=top]")
        INTF.placeBlockBatched(x - 13, y + 3, z + 19 + zz, slab2 + "[type=top]")
        INTF.placeBlockBatched(x + 13, y + 3, z - 14 - zz, slab2 + "[type=top]")
        INTF.placeBlockBatched(x + 13, y + 3, z - 19 - zz, slab2 + "[type=top]")
        INTF.placeBlockBatched(x + 13, y + 3, z + 14 + zz, slab2 + "[type=top]")
        INTF.placeBlockBatched(x + 13, y + 3, z + 19 + zz, slab2 + "[type=top]")

        INTF.placeBlockBatched(x + 19, y + 2, z - 5 - zz, mainBlock)
        INTF.placeBlockBatched(x - 19, y + 2, z - 5 - zz, mainBlock)
        INTF.placeBlockBatched(x + 19, y + 2, z + 5 + zz, mainBlock)
        INTF.placeBlockBatched(x - 19, y + 2, z + 5 + zz, mainBlock)
        INTF.placeBlockBatched(x + 9, y + 2, z + 10 + zz, mainBlock)
        INTF.placeBlockBatched(x + 9, y + 2, z + 15 + zz, mainBlock)
        INTF.placeBlockBatched(x + 9, y + 2, z - 10 - zz, mainBlock)
        INTF.placeBlockBatched(x + 9, y + 2, z - 15 - zz, mainBlock)
        INTF.placeBlockBatched(x - 9, y + 2, z + 10 + zz, mainBlock)
        INTF.placeBlockBatched(x - 9, y + 2, z + 15 + zz, mainBlock)
        INTF.placeBlockBatched(x - 9, y + 2, z - 10 - zz, mainBlock)
        INTF.placeBlockBatched(x - 9, y + 2, z - 15 - zz, mainBlock)
    for xx in range(7):
        INTF.placeBlockBatched(x - 3 + xx, y + 2, z - 24, stairBlocks + "[facing=south,half=bottom]")
        INTF.placeBlockBatched(x - 3 + xx, y + 1, z - 25, stairBlocks + "[facing=south,half=bottom]")
        INTF.placeBlockBatched(x - 3 + xx, y, z - 26, stairBlocks + "[facing=south,half=bottom]")

        for yy in range(2):
            INTF.placeBlockBatched(x - 3 + xx, y + yy, z - 24, accentBlock)
        INTF.placeBlockBatched(x - 3 + xx, y, z - 25, accentBlock)

    for xx in range(7):
        INTF.placeBlockBatched(x - 3 + xx, y + 2, z + 24, stairBlocks + "[facing=north,half=bottom]")
        INTF.placeBlockBatched(x - 3 + xx, y + 1, z + 25, stairBlocks + "[facing=north,half=bottom]")
        INTF.placeBlockBatched(x - 3 + xx, y, z + 26, stairBlocks + "[facing=north,half=bottom]")

        INTF.placeBlockBatched(x - 3 + xx, y + 2, z + 19, mainBlock)
        INTF.placeBlockBatched(x - 3 + xx, y + 2, z - 19, mainBlock)
        for yy in range(2):
            INTF.placeBlockBatched(x - 3 + xx, y + yy, z + 24, accentBlock)
        INTF.placeBlockBatched(x - 3 + xx, y, z + 25, accentBlock)

    for zz in range(7):
        INTF.placeBlockBatched(x + 24, y + 2, z - 3 + zz, stairBlocks + "[facing=west,half=bottom]")
        INTF.placeBlockBatched(x + 25, y + 1, z - 3 + zz, stairBlocks + "[facing=west,half=bottom]")
        INTF.placeBlockBatched(x + 26, y, z - 3 + zz, stairBlocks + "[facing=west,half=bottom]")

        INTF.placeBlockBatched(x + 19, y + 2, z - 3 + zz, mainBlock)
        INTF.placeBlockBatched(x - 19, y + 2, z - 3 + zz, mainBlock)
        for yy in range(2):
            INTF.placeBlockBatched(x + 24, y + yy, z - 3 + zz, accentBlock)
        INTF.placeBlockBatched(x + 25, y, z - 3 + zz, accentBlock)

    for zz in range(7):
        INTF.placeBlockBatched(x - 24, y + 2, z - 3 + zz, stairBlocks + "[facing=east,half=bottom]")
        INTF.placeBlockBatched(x - 25, y + 1, z - 3 + zz, stairBlocks + "[facing=east,half=bottom]")
        INTF.placeBlockBatched(x - 26, y, z - 3 + zz, stairBlocks + "[facing=east,half=bottom]")
        for yy in range(2):
            INTF.placeBlockBatched(x - 24, y + yy, z - 3 + zz, accentBlock)
        INTF.placeBlockBatched(x - 25, y, z - 3 + zz, accentBlock)

    for yy in range(3):
        INTF.placeBlockBatched(x - 4, y + yy, z - 24, accentBlock)
        INTF.placeBlockBatched(x + 4, y + yy, z - 24, accentBlock)
        INTF.placeBlockBatched(x - 4, y + yy, z + 24, accentBlock)
        INTF.placeBlockBatched(x + 4, y + yy, z + 24, accentBlock)
        INTF.placeBlockBatched(x - 24, y + yy, z - 4, accentBlock)
        INTF.placeBlockBatched(x - 24, y + yy, z + 4, accentBlock)
        INTF.placeBlockBatched(x + 24, y + yy, z - 4, accentBlock)
        INTF.placeBlockBatched(x + 24, y + yy, z + 4, accentBlock)
    for yy in range(2):
        INTF.placeBlockBatched(x - 4, y + yy, z - 25, accentBlock)
        INTF.placeBlockBatched(x + 4, y + yy, z - 25, accentBlock)
        INTF.placeBlockBatched(x - 4, y + yy, z + 25, accentBlock)
        INTF.placeBlockBatched(x + 4, y + yy, z + 25, accentBlock)
        INTF.placeBlockBatched(x - 25, y + yy, z - 4, accentBlock)
        INTF.placeBlockBatched(x - 25, y + yy, z + 4, accentBlock)
        INTF.placeBlockBatched(x + 25, y + yy, z - 4, accentBlock)
        INTF.placeBlockBatched(x + 25, y + yy, z + 4, accentBlock)
    INTF.placeBlockBatched(x - 4, y, z - 26, accentBlock)
    INTF.placeBlockBatched(x + 4, y, z - 26, accentBlock)
    INTF.placeBlockBatched(x - 4, y, z + 26, accentBlock)
    INTF.placeBlockBatched(x + 4, y, z + 26, accentBlock)
    INTF.placeBlockBatched(x - 26, y, z - 4, accentBlock)
    INTF.placeBlockBatched(x - 26, y, z + 4, accentBlock)
    INTF.placeBlockBatched(x + 26, y, z - 4, accentBlock)
    INTF.placeBlockBatched(x + 26, y, z + 4, accentBlock)

    INTF.placeBlockBatched(x - 4, y + 1, z - 26, lanternBlock)
    INTF.placeBlockBatched(x + 4, y + 1, z - 26, lanternBlock)
    INTF.placeBlockBatched(x - 4, y + 1, z + 26, lanternBlock)
    INTF.placeBlockBatched(x + 4, y + 1, z + 26, lanternBlock)
    INTF.placeBlockBatched(x - 26, y + 1, z - 4, lanternBlock)
    INTF.placeBlockBatched(x - 26, y + 1, z + 4, lanternBlock)
    INTF.placeBlockBatched(x + 26, y + 1, z - 4, lanternBlock)
    INTF.placeBlockBatched(x + 26, y + 1, z + 4, lanternBlock)

    INTF.placeBlockBatched(x - 4, y + 2, z - 25, lanternBlock)
    INTF.placeBlockBatched(x + 4, y + 2, z - 25, lanternBlock)
    INTF.placeBlockBatched(x - 4, y + 2, z + 25, lanternBlock)
    INTF.placeBlockBatched(x + 4, y + 2, z + 25, lanternBlock)
    INTF.placeBlockBatched(x - 25, y + 2, z - 4, lanternBlock)
    INTF.placeBlockBatched(x - 25, y + 2, z + 4, lanternBlock)
    INTF.placeBlockBatched(x + 25, y + 2, z - 4, lanternBlock)
    INTF.placeBlockBatched(x + 25, y + 2, z + 4, lanternBlock)

    INTF.placeBlockBatched(x - 4, y + 3, z - 24, lanternBlock)
    INTF.placeBlockBatched(x + 4, y + 3, z - 24, lanternBlock)
    INTF.placeBlockBatched(x - 4, y + 3, z + 24, lanternBlock)
    INTF.placeBlockBatched(x + 4, y + 3, z + 24, lanternBlock)
    INTF.placeBlockBatched(x - 24, y + 3, z - 4, lanternBlock)
    INTF.placeBlockBatched(x - 24, y + 3, z + 4, lanternBlock)
    INTF.placeBlockBatched(x + 24, y + 3, z - 4, lanternBlock)
    INTF.placeBlockBatched(x + 24, y + 3, z + 4, lanternBlock)

    for xx in range(17):
        for zz in range(37):
            INTF.placeBlockBatched(x - 8 + xx, y + 2, z - 18 + zz, accentBlock)
    for xx in range(10):
        for zz in range(17):
            INTF.placeBlockBatched(x + 9 + xx, y + 2, z - 8 + zz, accentBlock)
            INTF.placeBlockBatched(x - 9 - xx, y + 2, z - 8 + zz, accentBlock)
    for xx in range(7):
        INTF.placeBlockBatched(x - 3 + xx, y + 2, z + 9, mainBlock)
        INTF.placeBlockBatched(x - 3 + xx, y + 2, z - 9, mainBlock)
    for zz in range(7):
        INTF.placeBlockBatched(x + 9, y + 2, z - 3 + zz, mainBlock)
        INTF.placeBlockBatched(x - 9, y + 2, z - 3 + zz, mainBlock)
    for xx in range(4):
        INTF.placeBlockBatched(x - 5 - xx, y + 2, z + 9, mainBlock)
        INTF.placeBlockBatched(x - 5 - xx, y + 2, z - 9, mainBlock)
        INTF.placeBlockBatched(x + 5 + xx, y + 2, z + 9, mainBlock)
        INTF.placeBlockBatched(x + 5 + xx, y + 2, z - 9, mainBlock)
    for zz in range(4):
        INTF.placeBlockBatched(x + 9, y + 2, z + 5 + zz, mainBlock)
        INTF.placeBlockBatched(x - 9, y + 2, z + 5 + zz, mainBlock)
        INTF.placeBlockBatched(x + 9, y + 2, z - 5 - zz, mainBlock)
        INTF.placeBlockBatched(x - 9, y + 2, z - 5 - zz, mainBlock)

    # ladders from four sides
    buid_size = 26
    if INTF.getBlock(x+buid_size+1,y,z) != "minecraft:air":
        INTF.setBlock(x+buid_size,y,z,"ladder"+"[facing=west]")
        yy = y+1
        while INTF.getBlock(x+buid_size+1,yy,z) != "minecraft:air":
            INTF.setBlock(x+buid_size,yy,z,"ladder"+"[facing=west]")
            yy+=1

    elif INTF.getBlock(x+buid_size+1,y-2,z) == "minecraft:air":
            INTF.setBlock(x+buid_size+1,y-1,z,"ladder"+"[facing=east]")
            yy = y-2
            while INTF.getBlock(x+buid_size+1,yy,z) == "minecraft:air":
                INTF.setBlock(x+buid_size+1,yy,z,"ladder"+"[facing=east]")
                yy-=1


    if INTF.getBlock(x-buid_size-1,y,z) != "minecraft:air":
        INTF.setBlock(x-buid_size,y,z,"ladder"+"[facing=east]")
        yy = y+1
        while INTF.getBlock(x-buid_size-1,yy,z) != "minecraft:air":
            INTF.setBlock(x-buid_size,yy,z,"ladder"+"[facing=east]")
            yy+=1

    elif INTF.getBlock(x-buid_size-1,y-2,z) == "minecraft:air":
            INTF.setBlock(x-buid_size-1,y-1,z,"ladder"+"[facing=west]")
            yy = y-2
            while INTF.getBlock(x-buid_size-1,yy,z) == "minecraft:air":
                INTF.setBlock(x-buid_size-1,yy,z,"ladder"+"[facing=west]")
                yy-=1

    if INTF.getBlock(x,y,z+buid_size+1) != "minecraft:air":
        INTF.setBlock(x,y,z+buid_size,"ladder"+"[facing=north]")
        yy = y+1
        while INTF.getBlock(x,yy,z+buid_size+1) != "minecraft:air":
            INTF.setBlock(x,yy,z+buid_size,"ladder"+"[facing=north]")
            yy+=1

    elif INTF.getBlock(x,y-2,z+buid_size+1) == "minecraft:air":
            INTF.setBlock(x,y-1,z+buid_size+1,"ladder"+"[facing=south]")
            yy = y-2
            while INTF.getBlock(x,yy,z+buid_size+1) == "minecraft:air":
                INTF.setBlock(x,yy,z+buid_size+1,"ladder"+"[facing=south]")
                yy-=1

    if INTF.getBlock(x,y,z-buid_size-1) != "minecraft:air":
        INTF.setBlock(x,y,z-buid_size,"ladder"+"[facing=south]")
        yy = y+1
        while INTF.getBlock(x,yy,z-buid_size-1) != "minecraft:air":
            INTF.setBlock(x,yy,z-buid_size,"ladder"+"[facing=south]")
            yy+=1

    elif INTF.getBlock(x,y-2,z-buid_size-2) == "minecraft:air":
            INTF.setBlock(x,y-1,z-buid_size-1,"ladder"+"[facing=north]")
            yy = y-2
            while INTF.getBlock(x,yy,z-buid_size-2) == "minecraft:air":
                INTF.setBlock(x,yy,z-buid_size-1,"ladder"+"[facing=north]")
                yy-=1

    # place beaco in the center
    c = 0
    for i in range(-10,10):
        for j in range(-10,10):
            if i==-10 or i==10-1 or j==-10 or j==10-1:
                if c%3 == 0:
                    GEO.placeCuboid(x+i, y+3, z+j, x+i, y + 3, z+j, "beacon")
                c+=1
    



