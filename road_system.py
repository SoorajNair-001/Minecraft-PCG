import building_layout
from gdpc import interface as INTF
import matplotlib as mpl
from matplotlib import pyplot
import numpy as np
from gdpc import worldLoader as WL
from gdpc import geometry as GEO

STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA
WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)  # this takes a while



path_grid,num_spots = building_layout.buildLocations()
location_grid = path_grid.copy()
path_grid[5][(int)(path_grid.shape[1]/2)] = 1
path_grid[(int)(path_grid.shape[0]/2)][5] = 1
path_grid[path_grid.shape[0]-5][(int)(path_grid.shape[1]/2)] = 1
path_grid[(int)(path_grid.shape[0]/2)][path_grid.shape[1]-5] = 1

path_grid[(int)(path_grid.shape[0]/2)][(int)(path_grid.shape[1]/2)-30] = 1
path_grid[(int)(path_grid.shape[0]/2)-30][(int)(path_grid.shape[1]/2)] = 1
path_grid[(int)(path_grid.shape[0]/2)][(int)(path_grid.shape[1]/2)+30] = 1
path_grid[(int)(path_grid.shape[0]/2)+30][(int)(path_grid.shape[1]/2)] = 1

width = path_grid.shape[0]
height = path_grid.shape[1]

class Node:
  def __init__(self, x,y,depth,parent=None):
    self.x = x
    self.y = y
    self.depth = depth
    self.parent = parent


def bfs(sx,sy,goal):
    index = 0
    openList = []
    closedList = np.zeros((width,height))
    rootNode = Node(sx,sy,0,None)
    openList.append(rootNode)
    actions = [[0, -1], [0, 1], [-1, 0], [1, 0]]
    paths = []
    path = []
    while not (index == len(openList)):
        curr_node = openList[index]
        index+=1
        if(closedList[curr_node.x,curr_node.y] == 1):
            continue 
        closedList[curr_node.x,curr_node.y] = 1

        if [curr_node.x,curr_node.y] in goal:
            c_node = curr_node
            while True:
                path.append([c_node.x,c_node.y])
                c_node = c_node.parent
                if c_node.x==sx and c_node.y==sy:
                    break
            paths.append([curr_node.x,curr_node.y,curr_node.depth,path])
            path = []

        # Going through all actions
        for action in actions:
            nx = curr_node.x + action[0]
            ny = curr_node.y + action[1]
            # checking if within bound and the grid element is not red
            if(not(nx>=0 and nx<width and ny>=0 and ny<height)):
                continue
            # create child
            newnode = Node(nx,ny,(curr_node.depth)+1,curr_node)
            openList.append(newnode); #add child to openlist
    return paths


class Spot:
    def __init__(self,x,y,paths):
        self.x = x
        self.y = y
        self.paths = paths

# attribution: https://www.programiz.com/dsa/prim-algorithm
def minimumSpanningRoad():
    
    spotObjs = []
    spots = []
    for i in range(2,width-2):
        for j in range(2,height-2):
            if path_grid[i][j] == 1:
                spots.append([i,j])

    for spot in spots:
        a = spots.copy()
        a.remove(spot)
        paths = bfs(spot[0],spot[1],a)
        spotObjs.append(Spot(spot[0],spot[1],paths))

    # distance matrix
    dist_matix = []
    for spot in spotObjs:
        row = []
        for i in range(0,len(spots)):
            for j in range(0,len(spot.paths)):
                if spots[i][0] == spot.paths[j][0] and spots[i][1] == spot.paths[j][1]:
                    row.append(spot.paths[j][2])
            if spots[i][0] == spot.x and spots[i][1] == spot.y:
                row.append(999999999)
        dist_matix.append(row)

    # minimum spanning tree       
    INF = 999999999999
    V = len(dist_matix)
    G = dist_matix
    selected = np.zeros(len(dist_matix))
    no_edge = 0 # set number of edge to 0
    selected[0] = True
    # find the edges
    while (no_edge < V - 1):
        minimum = INF
        x = 0
        y = 0
        for i in range(V):
            if selected[i]:
                for j in range(V):
                    if ((not selected[j]) and G[i][j]):  
                        # not in selected and there is an edge
                        if minimum > G[i][j]:
                            minimum = G[i][j]
                            x = i
                            y = j     
        spot1 = spotObjs[x]
        spot2 = spotObjs[y]
        for path in spot1.paths:
            if path[0]==spot2.x and path[1]==spot2.y:
                path_bet = path[3]
                for ele in path_bet:
                    path_grid[ele[0],ele[1]] = 1
                    
        selected[y] = True
        no_edge += 1

    for n in range(4,5):
        path_grid[n][(int)(path_grid.shape[1]/2)] = 1
        path_grid[(int)(path_grid.shape[0]/2)][n] = 1
        path_grid[path_grid.shape[0]-n][(int)(path_grid.shape[1]/2)] = 1
        path_grid[(int)(path_grid.shape[0]/2)][path_grid.shape[1]-n] = 1

    return path_grid



def buildRoads(biome):
    print("Building roads..")
    # biome blocks
    if 'desert' in biome:
        pathBlock = "smooth_red_sandstone"
    elif 'ocean' in biome:
        pathBlock = "glass"
    elif 'forest' in biome:
        pathBlock = "oak_planks"
    elif 'taiga' in biome:
        pathBlock = "oak_planks"
    elif 'snowy' in biome:
        pathBlock = "packed_ice"

    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    roads = minimumSpanningRoad()

    # height of each road location
    roadHights = np.zeros((abs(ENDX - STARTX),abs(ENDZ - STARTZ)))
    roadHights2d = []
    for i in range(0,abs(ENDX - STARTX)):
        for j in range(0,abs(ENDZ - STARTZ)):
            if(roads[i][j]==1):
                roadHights[i][j] = heights[(i,j)]
                roadHights2d.append(heights[(i,j)])
    mHeight = int(np.median(roadHights2d))
    print("median height:",mHeight)
    
    for i in range(0,abs(ENDX - STARTX)):
        for j in range(0,abs(ENDZ - STARTZ)):
            if(roads[i][j]==1):
                # steep cliff
                if roadHights[i][j] > mHeight+7:
                    roadHights[i][j] = mHeight+7
                # trenches
                if roadHights[i][j] < mHeight-5:
                    roadHights[i][j] = mHeight-5
    
    # cardinal median smoothing
    for i in range(0,abs(ENDX - STARTX)):
        for j in range(0,abs(ENDZ - STARTZ)):
            if(roads[i][j]==1):
                neighbourH = []
                if i-1>=0:
                    if roads[i-1][j]==1:
                        neighbourH.append(roadHights[i-1][j])
                if i+1<=len(roads):
                    if roads[i+1][j]==1:
                        neighbourH.append(roadHights[i+1][j])
                if j-1>=0:
                    if roads[i][j-1]==1:
                        neighbourH.append(roadHights[i][j-1])
                if j+1<=len(roads[0]):
                    if roads[i][j+1]==1:
                        neighbourH.append(roadHights[i][j+1])
                newH = int(np.median(neighbourH))
                roadHights[i][j] = newH
    
    # placing road blocks
    for i in range(0,abs(ENDX - STARTX)):
        for j in range(0,abs(ENDZ - STARTZ)):
            if(roads[i][j]==1):
                y = int(roadHights[i][j])
                for x1 in range(-4,4):
                    for y1 in range(-4,4):
                        GEO.placeCuboid(STARTX+i+x1, y, STARTZ+j+y1, STARTX+i+x1, y + 10, STARTZ+j+y1, "air")
                        if (    INTF.getBlock(STARTX+i+x1, y + 1, STARTZ+j+y1)!="minecraft:air"
                            and INTF.getBlock(STARTX+i+x1, y + 2, STARTZ+j+y1)!="minecraft:air"
                            and INTF.getBlock(STARTX+i+x1, y + 3, STARTZ+j+y1)!="minecraft:air"
                            and INTF.getBlock(STARTX+i+x1, y + 4, STARTZ+j+y1)!="minecraft:air"
                            and INTF.getBlock(STARTX+i+x1, y + 5, STARTZ+j+y1)!="minecraft:air"
                            and INTF.getBlock(STARTX+i+x1, y + 6, STARTZ+j+y1)!="minecraft:air"
                            and INTF.getBlock(STARTX+i+x1, y + 7, STARTZ+j+y1)!="minecraft:air"
                            and INTF.getBlock(STARTX+i+x1, y + 8, STARTZ+j+y1)!="minecraft:air"
                            and INTF.getBlock(STARTX+i+x1, y + 9, STARTZ+j+y1)!="minecraft:air"
                            and INTF.getBlock(STARTX+i+x1, y + 10, STARTZ+j+y1)!="minecraft:air"
                            and INTF.getBlock(STARTX+i+x1, y + 11, STARTZ+j+y1)!="minecraft:air"
                            and INTF.getBlock(STARTX+i+x1, y + 12, STARTZ+j+y1)!="minecraft:air"):
                            INTF.placeBlock(STARTX+i+x1, y + 11, STARTZ+j+y1,"lantern"+"[hanging=true]")
                        GEO.placeCuboid(STARTX+i+x1, y-1, STARTZ+j+y1, STARTX+i+x1, y-1, STARTZ+j+y1, pathBlock)
                                       
    return location_grid,roadHights,num_spots


