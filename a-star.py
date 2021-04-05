import sys
import math

X_MAX = 10
Y_MAX = 10
X = 0
Y = 1

class Node:
    def __init__(self):
        # tuple containing the x- and y-coordinates of this node
        self.location = (-1,-1)
        
        # tuple containing the x- and y-coordinates of parent node
        self.parent = (-1,-1)

        # path costs
        self.f = float("inf")
        self.g = float("inf")
        self.h = float("inf")
    
    # Euclidean Distance heuristic (distance formula) to calculate h-cost
    def calculate_h(self, destination):
        x_dist = destination[X] - self.location[X]
        y_dist = destination[Y] - self.location[Y]
        return math.sqrt( x_dist*x_dist + y_dist*y_dist )


# utility function to determine if current position is within given grid
def isValid(loc):
    return (loc[X] >= 0) and (loc[X] < X_MAX) and (loc[Y] >= 0) and (loc[Y] < Y_MAX)

# utility function to determine if a current position is able to be traversed
def isUnBlocked(grid, loc):
    # orientation is switched so that grid can be written as row, col and algorithm can be written in x, y format
    return grid[loc[Y]][loc[X]] == 0

# utility function to determine if search algorithm has reached the goal node
def isDestination(loc, dest):
    return (loc[X] == dest[X]) and (loc[Y] == dest[Y])

# utility function to determine the distance from source to destination node
def tracePath(nodes, dest):
    path = []

    # follow parent pointers until source node is reached
    curr = dest
    curr_x = dest[X]
    curr_y = dest[Y]
    while not (nodes[curr_x][curr_y].parent == (curr_x,curr_y)):
        curr_x = curr[X]
        curr_y = curr[Y]
        
        # add current node to path
        path.append(curr)

        # update current node to its parent
        curr = nodes[curr_x][curr_y].parent

    return path

def aStarSearch(grid, source, dest):
    # validate source and destination nodes
    if not isValid(source):
        print("invalid source node")
        return None
    if not isValid(dest):
        print("invalid destination node")
        return None
    if (not isUnBlocked(grid, source)) or (not isUnBlocked(grid, dest)):
        print("source or destination is blocked")
        return None
    
    # if already at destination
    if (isDestination(source, dest)):
        print("already at destination")
        return None
    
    # initialize a list containing the information for each cell in the grid (using Node objects)
    nodes = []
    for i in range(X_MAX):
        nodes.append([])
        for j in range(Y_MAX):
            node = Node()
            node.location = (i,j)

            nodes[i].append(node)

    # initialize the parameters of source node
    curr_x = source[X]
    curr_y = source[Y]
    nodes[curr_x][curr_y].f = 0
    nodes[curr_x][curr_y].g = 0
    nodes[curr_x][curr_y].h = 0
    nodes[curr_x][curr_y].parent = (curr_x,curr_y)

    # declare closed list and initialize all values with False
    closed_list = []
    for i in range(X_MAX):
        closed_list.append([])
        for j in range(Y_MAX):
            closed_list[i].append(False)
    
    # declare open list and initialize with source node
    # open list tuple format: ( f-cost, (x-location,y-location) )
    open_list = []
    open_list.append( ( 0,(curr_x,curr_y) ) )

    # look through open list until either destination is found or there aren't any more valid nodes to visit
    found_dest = False
    while len(open_list) != 0:
        # get the first element in open list
        curr = open_list[0]
        curr_x = curr[1][X]
        curr_y = curr[1][Y]

        # remove curr from open list
        open_list.pop(0)

        # show that curr has been visited in closed list
        closed_list[curr_x][curr_y] = True

        # get successor nodes (8 possible-if unobstructed)
        # possible locations are N, NE, E, SE, S, SW, W, NW
        possible_locations = [(curr_x,curr_y-1), (curr_x+1,curr_y-1), (curr_x+1,curr_y),
                            (curr_x+1,curr_y+1), (curr_x,curr_y+1), (curr_x-1,curr_y+1),
                            (curr_x-1,curr_y), (curr_x-1,curr_y-1)]
        
        # add valid successors to open list and check if destination has been reached
        for successor_loc in possible_locations:
            succ_x = successor_loc[X]
            succ_y = successor_loc[Y]

            if (isValid(successor_loc)):
                if isDestination(successor_loc, dest):
                    nodes[succ_x][succ_y].parent = (curr_x,curr_y)
                    found_dest = True
                    return tracePath(nodes, dest)
                elif (closed_list[succ_x][succ_y] == False) and (isUnBlocked(grid,successor_loc)):
                    # diagonal to current node
                    gNew = nodes[curr_x][curr_y].g
                    if succ_x != curr_x and succ_y != curr_y:
                        gNew += 1.4
                    # perpendicular to current node
                    else:
                        gNew += 1
                    hNew = nodes[succ_x][succ_y].calculate_h(dest)
                    fNew = gNew + hNew

                    # add this successor to open list if
                    # - it isn't already on there
                    # - it is a better location (smaller f-cost)
                    if (nodes[succ_x][succ_y].f == float("inf")) or (nodes[succ_x][succ_y].f > fNew):
                        open_list.append((fNew,successor_loc))

                        # update this node's information
                        nodes[succ_x][succ_y].f = fNew
                        nodes[succ_x][succ_y].g = gNew
                        nodes[succ_x][succ_y].h = hNew
                        nodes[succ_x][succ_y].parent = (curr_x,curr_y)
    
    # algorithm was unable to find destination from the current source
    if found_dest == False:
        print("Failed to find the destination!")
        return None

# utility function that generates a grid of 1's and 0's
def gen_grid():
    grid = [
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,1,1,1,0,0,0,0,0],
        [1,1,0,0,1,0,0,0,0,0],
        [0,1,1,1,1,1,1,1,0,0],
        [0,0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,1,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
    ]
    return grid

# utility function that prints a grid of 1's and 0's with a path from source to destination
def print_grid(grid, path):
    for i in range(X_MAX+2):
        sys.stdout.write('=')
    sys.stdout.write('\n')

    for r in range(len(grid)):
        sys.stdout.write('|')
        for c in range(len(grid[r])):
            if (c,r) in path:
                sys.stdout.write('*')
            elif grid[r][c] == 0:
                sys.stdout.write(' ')
            else:
                sys.stdout.write('X')
        
        sys.stdout.write('|\n')

    for i in range(X_MAX+2):
        sys.stdout.write('=')
    sys.stdout.write('\n')
    
if __name__ == "__main__":
    grid = gen_grid()
    source = (0,0)
    destination = (X_MAX-1, Y_MAX-1)

    path = aStarSearch(grid, source, destination)

    if path != None:
        print_grid(grid,path)
    
    
    
