from gdpc import interface as INTF
import matplotlib as mpl
from matplotlib import pyplot
import numpy as np
import random
from gdpc import worldLoader as WL
from gdpc import geometry as GEO

import castle

STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()
WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)  # this takes a while

# find spots to build buildings using Perlin Noise
def buildLocations():
    grid = np.zeros((abs(ENDX - STARTX),abs(ENDZ - STARTZ)))
    width = grid.shape[0]
    height = grid.shape[1]
    noise = generateWhiteNoise(grid)
    octaveCount = 3
    perlinNoise = generatePerlinNoise(noise,octaveCount)

    spots_gap = 18
    spots = np.zeros((width,height))
    for i in range(12,width-12):
        for j in range(12,height-12):
            if perlinNoise[i][j] > 0.9:
                spots[i][j] = 1

    # removing center points for castle placement
    centerx= (int)(width/2)
    centery= (int)(height/2)
    for i in range(-50,50):
        for j in range(-50,50):
            spots[centerx+i][centery+j] = 0
    
    # kernal filtering
    for i in range(0,width):
        for j in range(0,height):
            count = 0
            if spots[i][j] == 1: 
                for x in range(i-spots_gap,i+spots_gap):
                    for y in range(j-spots_gap,j+spots_gap):
                        if x>=0 and x<width and y>=0 and y<height:
                            if spots[x][y] == 1:
                                count += 1
            if count>1:
                for x in range(i-spots_gap,i+spots_gap):
                    for y in range(j-spots_gap,j+spots_gap):
                        if x>=0 and x<width and y>=0 and y<height:
                            spots[x][y] = 0
                spots[i][j] = 1

    sum_spots = 0
    for i in range(0,width):
        for j in range(0,height):
            if spots[i][j] == 1:
                sum_spots += 1
    print(sum_spots,"buildings will be created..")

    return spots,sum_spots

# attribution - http://devmag.org.za/2009/04/25/perlin-noise/
def generateWhiteNoise(grid):
    width = grid.shape[0]
    height = grid.shape[1]
    noise = np.random.rand(width,height)
    return noise

# attribution - http://devmag.org.za/2009/04/25/perlin-noise/
def interpolate(x0, x1, alpha):
    return x0 * (1 - alpha) + alpha * x1

# attribution - http://devmag.org.za/2009/04/25/perlin-noise/
def generateSmoothNoise(baseNoise,octave):
    width = baseNoise.shape[0]
    height = baseNoise.shape[1]
    
    smoothNoise = np.zeros((width,height))
    
    samplePeriod = 1 << octave; # calculates 2 ^ k
    sampleFrequency = 1.0 / samplePeriod
    
    for i in range(0,width):
        #calculate the horizontal sampling indices
        sample_i0 = (int)(i / samplePeriod) * samplePeriod
        sample_i1 = (int)(sample_i0 + samplePeriod) % width #wrap around
        horizontal_blend = (float)(i - sample_i0) * sampleFrequency

        for j in range(0,height):
            #calculate the vertical sampling indices
            sample_j0 = (int)(j / samplePeriod) * samplePeriod
            sample_j1 = (int)(sample_j0 + samplePeriod) % height #wrap around
            vertical_blend = (float)(j - sample_j0) * sampleFrequency

            #blend the top two corners
            top = interpolate(baseNoise[sample_i0,sample_j0],baseNoise[sample_i1,sample_j0], horizontal_blend)

            #blend the bottom two corners
            bottom = interpolate(baseNoise[sample_i0,sample_j1],baseNoise[sample_i1,sample_j1], horizontal_blend)

            #final blend
            smoothNoise[i,j] = interpolate(top, bottom, vertical_blend)
    return smoothNoise

# attribution - http://devmag.org.za/2009/04/25/perlin-noise/
def generatePerlinNoise(baseNoise,octaveCount):
    width = baseNoise.shape[0]
    height = baseNoise.shape[1]
 
    smoothNoise = []
 
    persistance = 0.5
 
    #generate smooth noise
    for i in range(0,octaveCount):
        smoothNoise.append(generateSmoothNoise(baseNoise, i))
 
    perlinNoise = np.zeros((width,height))
    amplitude = 1.0
    totalAmplitude = 0.0
 
    #blend noise together
    for octave in range(octaveCount - 1, -1, -1):
        amplitude *= persistance
        totalAmplitude += amplitude
        for i in range(0,width):
            for j in range(0,height):
                perlinNoise[i,j] += (smoothNoise[octave][i,j] * amplitude)

    #normalisation
    for i in range(0,width):
        for j in range(0,height):
            pnoise = perlinNoise[i,j]
            perlinNoise[i,j] = pnoise/totalAmplitude

    return perlinNoise

# place foundations on spots
def placeBuildingFoundation(location_grid,roadHeights,biome):
    print("building foundations..")
    buid_size = 10
    # biome blocks
    if 'desert' in biome:
        foundationBlock = "sandstone"
        foundationBlockBorder = "sandstone"
    elif 'ocean' in biome:
        foundationBlock = "glass"
        foundationBlockBorder = "glass"
    elif 'forest' in biome:
        foundationBlock = "infested_mossy_stone_bricks"
        foundationBlockBorder = "chiseled_stone_bricks"
    elif 'taiga' in biome:
        foundationBlock = "infested_mossy_stone_bricks"
        foundationBlockBorder = "chiseled_stone_bricks"
    elif 'snowy' in biome:
        foundationBlock = "snow_block"
        foundationBlockBorder = "snow_block"

    for i in range(0,len(location_grid)):
        for j in range(0,len(location_grid[0])):
            if(location_grid[i][j]==1):
                y = (int)(roadHeights[i][j])      
                for x1 in range(-buid_size,buid_size):
                    for y1 in range(-buid_size,buid_size):
                        GEO.placeCuboid(STARTX+i+x1, y, STARTZ+j+y1, STARTX+i+x1, y + 15, STARTZ+j+y1, "air")
                        if INTF.getBlock(STARTX+i+x1, y + 16, STARTZ+j+y1)!="minecraft:air":
                            INTF.placeBlock(STARTX+i+x1, y + 16, STARTZ+j+y1,"lantern"+"[hanging=true]")
                for x1 in range(-buid_size,buid_size):
                    for y1 in range(-buid_size,buid_size):
                        if x1 == -buid_size or y1 == -buid_size or x1 == buid_size-1 or y1 == buid_size-1:
                            GEO.placeCuboid(STARTX+i+x1, y-1, STARTZ+j+y1, STARTX+i+x1, y - 1, STARTZ+j+y1, foundationBlockBorder)
                        else:GEO.placeCuboid(STARTX+i+x1, y-1, STARTZ+j+y1, STARTX+i+x1, y - 1, STARTZ+j+y1, foundationBlock)
                x = STARTX+i
                z = STARTZ+j
                if INTF.getBlock(x+buid_size,y,z) != "minecraft:air":
                    INTF.placeBlock(x+buid_size-1,y,z,"ladder"+"[facing=west]")
                    yy = y+1
                    while INTF.getBlock(x+buid_size,yy,z) != "minecraft:air":
                        INTF.placeBlock(x+buid_size-1,yy,z,"ladder"+"[facing=west]")
                        yy+=1

                elif INTF.getBlock(x+buid_size,y-2,z) == "minecraft:air":
                        INTF.placeBlock(x+buid_size,y-1,z,"ladder"+"[facing=east]")
                        yy = y-2
                        while INTF.getBlock(x+buid_size,yy,z) == "minecraft:air":
                            INTF.placeBlock(x+buid_size,yy,z,"ladder"+"[facing=east]")
                            yy-=1

                if INTF.getBlock(x-buid_size-1,y,z) != "minecraft:air":
                    INTF.placeBlock(x-buid_size,y,z,"ladder"+"[facing=east]")
                    yy = y+1
                    while INTF.getBlock(x-buid_size-1,yy,z) != "minecraft:air":
                        INTF.placeBlock(x-buid_size,yy,z,"ladder"+"[facing=east]")
                        yy+=1

                elif INTF.getBlock(x-buid_size-1,y-2,z) == "minecraft:air":
                        INTF.placeBlock(x-buid_size-1,y-1,z,"ladder"+"[facing=west]")
                        yy = y-2
                        while INTF.getBlock(x-buid_size-1,yy,z) == "minecraft:air":
                            INTF.placeBlock(x-buid_size-1,yy,z,"ladder"+"[facing=west]")
                            yy-=1

                if INTF.getBlock(x,y,z+buid_size) != "minecraft:air":
                    INTF.placeBlock(x,y,z+buid_size-1,"ladder"+"[facing=north]")
                    yy = y+1
                    while INTF.getBlock(x,yy,z+buid_size) != "minecraft:air":
                        INTF.placeBlock(x,yy,z+buid_size-1,"ladder"+"[facing=north]")
                        yy+=1

                elif INTF.getBlock(x,y-2,z+buid_size) == "minecraft:air":
                        INTF.placeBlock(x,y-1,z+buid_size,"ladder"+"[facing=south]")
                        yy = y-2
                        while INTF.getBlock(x,yy,z+buid_size) == "minecraft:air":
                            INTF.placeBlock(x,yy,z+buid_size,"ladder"+"[facing=south]")
                            yy-=1

                if INTF.getBlock(x,y,z-buid_size-1) != "minecraft:air":
                    INTF.placeBlock(x,y,z-buid_size,"ladder"+"[facing=south]")
                    yy = y+1
                    while INTF.getBlock(x,yy,z-buid_size-1) != "minecraft:air":
                        INTF.placeBlock(x,yy,z-buid_size,"ladder"+"[facing=south]")
                        yy+=1

                elif INTF.getBlock(x,y-2,z-buid_size-1) == "minecraft:air":
                        INTF.placeBlock(x,y-1,z-buid_size-1,"ladder"+"[facing=north]")
                        yy = y-2
                        while INTF.getBlock(x,yy,z-buid_size-1) == "minecraft:air":
                            INTF.placeBlock(x,yy,z-buid_size-1,"ladder"+"[facing=north]")
                            yy-=1

    