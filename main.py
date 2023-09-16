# /setbuildarea ~-75 0 ~-75 ~75 255 ~75
# /setbuildarea ~-100 0 ~-100 ~100 255 ~100
import random

from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL

import road_system
import build_perimeter
import building_layout
import castle

import house_L
import house_s
import barn
import store
import farm
import biomeFeature
import harbour


# build area 
STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA
# world slide
WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)  # this takes a while

def main():
    try:
        # height map
        heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
        
        # find primary biome
        biome = WORLDSLICE.getPrimaryBiomeNear(0, 100 , 0)[0]
        
        # center of the area
        centerx = abs(ENDX - STARTX)//2 
        centerz = abs(ENDZ - STARTZ)//2
        y = heights[(centerx,centerz)]
        x = STARTX + (ENDX - STARTX) // 2 
        z = STARTZ + (ENDZ - STARTZ) // 2
        
        print("Biome:",biome) # print biome
        if not (('desert' in biome) or ('ocean' in biome) or ('forest' in biome) 
            or ('taiga' in biome) or ('snowy' in biome)):
            print("Biome not recognized. Move to Desert or Ocean or Forest or Taiga or Snowy")
            return 0
            


        # build walls
        build_perimeter.buildWalls(biome)

        # build roads
        location_grid,roadHeights,num_spots = road_system.buildRoads(biome)
        
        # build foundations
        building_layout.placeBuildingFoundation(location_grid,roadHeights,biome)
        
        # build castle
        castle.buildCastle(x,y,z,biome)

        # place harbours near water bodies
        harbour.buildHarbor(location_grid)

        # place buildings in random order
        print("placing buildings..")
        build_spots = []
        for i in range(0,len(location_grid)):
            for j in range(0,len(location_grid[0])):
                if location_grid[i][j] == 1:
                    build_spots.append([0,i,j])   
        building = []
        # biome features(10%)
        for i in range(int(0.1*len(build_spots))):
            building.append(5)
        # barn(10%)
        for i in range(int(0.1*len(build_spots))):
            building.append(2)
        # store(10%)
        for i in range(int(0.1*len(build_spots))):
            building.append(3)
        # farm(10%)
        for i in range(int(0.1*len(build_spots))):
            building.append(4)
        # smallhouse(35%)
        for i in range(int(0.35*len(build_spots))):
            building.append(0)
        # largehouse(25%)
        for i in range(int(0.25*len(build_spots))):
            building.append(1)
        # filling rest with small houses
        while len(building)<len(build_spots):
            building.append(0)

        random.shuffle(building) # randomly shuffle the buildings
        
        for i in range(0,len(build_spots)):
            build_spots[i][0] = building[i]
        
        # place building in the random spots
        for spot in build_spots:
            x = spot[1]
            z = spot[2]
            y = int(roadHeights[x][z]) 
            if spot[0]==0:house_s.buildSqHouse(STARTX+x, y-1, STARTZ+z,biome) # small houses
            elif spot[0]==1:house_L.buildLHouse(STARTX+x, y-1, STARTZ+z,biome) # large houses
            elif spot[0]==2: barn.buildBarn(STARTX+x, y-1, STARTZ+z,biome) # barns
            elif spot[0]==3: store.buildStore(STARTX+x, y-1, STARTZ+z,biome) # shops
            elif spot[0]==4: farm.buildFarm(STARTX+x, y-1, STARTZ+z) # farms
            elif spot[0]==5: 
                # biome features
                if 'desert' in biome:
                    biomeFeature.deserts(STARTX+x, y-1, STARTZ+z)
                elif 'ocean' in biome:
                    biomeFeature.oceans(STARTX+x, y-1, STARTZ+z)
                elif 'forest' in biome:
                    biomeFeature.taiga_forest(STARTX+x, y-1, STARTZ+z)
                elif 'taiga' in biome:
                    biomeFeature.taiga_forest(STARTX+x, y-1, STARTZ+z)
                elif 'snowy' in biome:
                    biomeFeature.snowy_tundra(STARTX+x, y-1, STARTZ+z)

        print("Done!")
    except KeyboardInterrupt: 
        print("Pressed Ctrl-C to kill program.")

if __name__ == '__main__': main()
