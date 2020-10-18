import math
from heapq import heappop, heappush

def find_path (source_point, destination_point, mesh):

    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists []
        A list of boxes explored by the algorithm {}
    """
    path = []
    boxes = {}
    #bfsqueue = queue.Queue(0)
    #bfsqueue.put([source_point, None])                  #[node, previous]
    
    
    source_box = ()
    dest_box = ()
    for box in mesh['boxes']:                           #get the box for source_point and destination_point
        if point_within_box(source_point, box):
            source_box = box
        if point_within_box(destination_point, box):
            dest_box = box

    queue = [(0, source_box)]

    distances = {}
    distances[source_point] = 0

    backpointers = {}
    backpointers[source_point] = None

    while queue:                                        #breadth first search
        current_dist, current_box = heappop(queue)
        distances[current_box] = 1
        current_box_value = box_of_point(mesh, current_box)
        print(current_box, 'current box')
        print(current_box_value, 'box value')
        if(current_box_value == dest_box):
            print('gottem')
            #return path
        else:
            for adj_box in mesh['adj'][current_box_value]:
                pathcost = euclidean(current_box, box_center(adj_box)) + current_dist
                if adj_box not in backpointers or pathcost < distances[adj_box]:
                    distances[adj_box] = pathcost
                    backpointers[adj_box] = current_box
                    heappush(queue, (pathcost, adj_box))
    return path, boxes.keys()

def point_within_box(point, box):                       #check if a point is within a given box
    if box[0] < point[0] and box[1] < point[0] and box[2] > point[1] and box[3] > point[1]:
        return True
    else:
        return False

def box_of_point(mesh, point):
    for box in mesh['boxes']:                           #get the box for a given point
        if point_within_box(point, box):
            return box
    return False

def euclidean(tupleA, tupleB):
    base1 = (tupleA[0] - tupleB[0])
    base1 *= base1
    #print(base1)
    base2 = (tupleA[1] - tupleB[1])
    base2 *= base2
    #print(base2)
    return math.sqrt(base1+base2)


def findDetailPoint(boxA, boxB, originPoint):
    bAx1 = boxA[0]
    bAx2 = boxA[1]
    bAy1 = boxA[2]
    bAy2 = boxA[3]

    bBx1 = boxB[0]
    bBx2 = boxB[1]
    bBy1 = boxB[2]
    bBy2 = boxB[3]

    maxX, minX = [max(bAx1, bBx1), min(bAx2, bBx2)]
    maxY, minY = [max(bAy1, bBy1), min(bAy2, bBy2)]

    
    distanceA = euclidean(originPoint, (minX, minY))
    distanceB = euclidean(originPoint, (maxX, maxY))

    if minX == maxX: #vertical
        if distanceA < distanceB:
            return (minX, minY)
        elif distanceB < distanceB:
            return (maxX, maxY)
        else:
            newX = minX + ((maxX - minX)/2)
            return (newX, originPoint[1])
    if minY == maxY: #horizontal
        if distanceA < distanceB:
            return (minX, minY)
        elif distanceB < distanceB:
            return (maxX, maxY)
        else:
            newY = minY + ((maxY - minY)/2)
            return (originPoint[0], newY)

def box_center(box):
    return ((box[0] + box[2])/2, (box[1] + box[3])/2)