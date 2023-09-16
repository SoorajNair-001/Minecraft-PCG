from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL

STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()
WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)
wallBlock = "stone_brick_wall"
baseBlock = "stone_bricks"
def buildWalls(biome):
    # biome blocks
    if 'desert' in biome:
        wallBlock = "red_sandstone_wall"
        baseBlock = "chiseled_red_sandstone"
    elif 'ocean' in biome:
        wallBlock = "prismarine_wall"
        baseBlock = "prismarine_bricks"
    elif 'forest' in biome:
        wallBlock = "mossy_stone_brick_wall"
        baseBlock = "infested_mossy_stone_bricks"
    elif 'taiga' in biome:
        wallBlock = "mossy_stone_brick_wall"
        baseBlock = "infested_mossy_stone_bricks"
    elif 'snowy' in biome:
        wallBlock = "ice"
        baseBlock = "packed_ice"
        
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

    sumY = 0
    for x1 in range(STARTX, ENDX + 1):
        sumY += heights[(x1 - STARTX, 0)]
    avgY1 = (int) (sumY/(ENDX - STARTX))
    
    sumY = 0
    for x1 in range(STARTX, ENDX + 1):
        sumY += heights[(x1 - STARTX, ENDZ - STARTZ)]
    avgY2 = (int) (sumY/(ENDX - STARTX))

    sumZ = 0
    for z1 in range(STARTZ, ENDZ + 1):
        sumZ += heights[(0, z1 - STARTZ)]
    avgY3 = (int) (sumZ/(ENDZ - STARTZ))

    sumZ = 0
    for z1 in range(STARTZ, ENDZ + 1):
        sumZ += heights[(ENDX - STARTX, z1 - STARTZ)]
    avgY4 = (int) (sumZ/(ENDZ - STARTZ))

    avgY = (int)((avgY1+avgY2+avgY3+avgY4)/4)

    y = avgY
    print("Building walls..")
    # building the east-west walls
    for x in range(STARTX, ENDX + 1):
        if (x!= (STARTX+(ENDX-STARTX)//2)-3 and x!= (STARTX+(ENDX-STARTX)//2)-2 
            and x!= (STARTX+(ENDX-STARTX)//2)-1 and x!= (STARTX+(ENDX-STARTX)//2) 
            and x!= (STARTX+(ENDX-STARTX)//2)+1 and x!= (STARTX+(ENDX-STARTX)//2)+2 
            and x!= (STARTX+(ENDX-STARTX)//2)+3):
            # the northern wall
            GEO.placeCuboid(x, heights[(x - STARTX, 0)] -1, STARTZ+0, x, y + 2, STARTZ+0, baseBlock)
            GEO.placeCuboid(x, y + 2, STARTZ+0, x, y + 10, STARTZ+0, wallBlock )
                
            # the southern wall
            GEO.placeCuboid(x, heights[(x - STARTX, ENDZ - STARTZ)] -1, ENDZ-0, x, y + 2, ENDZ-0, baseBlock)
            GEO.placeCuboid(x, y + 2, ENDZ-0, x, y + 10, ENDZ-0, wallBlock )
        
    # building the north-south walls
    for z in range(STARTZ, ENDZ + 1):
        if (z!= (STARTZ+(ENDZ-STARTZ)//2)-3 and z!= (STARTZ+(ENDZ-STARTZ)//2)-2 
            and z!= (STARTZ+(ENDZ-STARTZ)//2)-1 and z!= (STARTZ+(ENDZ-STARTZ)//2) 
            and z!= (STARTZ+(ENDZ-STARTZ)//2)+1 and z!= (STARTZ+(ENDZ-STARTZ)//2)+2 
            and z!= (STARTZ+(ENDZ-STARTZ)//2)+3):
            # the western wall
            GEO.placeCuboid(STARTX+0, heights[(0, z - STARTZ)] -1, z, STARTX+0, y + 2, z, baseBlock)
            GEO.placeCuboid(STARTX+0, y + 2, z, STARTX+0, y + 10, z, wallBlock )
            
            # the eastern wall
            GEO.placeCuboid(ENDX-0, heights[(ENDX - STARTX, z - STARTZ)] -1, z, ENDX-0, y + 2, z, baseBlock)
            GEO.placeCuboid(ENDX-0, y + 2, z, ENDX-0, y + 10, z, wallBlock )
