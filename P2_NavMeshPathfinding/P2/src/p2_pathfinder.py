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

    source_box = ()
    dest_box = ()
    for box in mesh['boxes']:                           #get the box for source_point and destination_point
        if point_within_box(source_point, box):
            source_box = box
        if point_within_box(destination_point, box):
            dest_box = box

    if source_box == () or dest_box == () or source_box == None or dest_box == None:
        print("No path possible")
        return (path, boxes.keys())
    elif(source_box == dest_box):
        boxes[source_box] = dest_box
        return ([source_point, destination_point], boxes.keys())
    elif source_box in mesh['adj'][dest_box]:
        boxes[source_box] = dest_box
        boxes[dest_box] = source_box
        return([source_point, findDetailPoint(source_box, dest_box, source_point), destination_point], boxes.keys())

    queue = [(0, source_box, 'destination')]
    heappush(queue, (0, dest_box, 'source'))

    detail_points = {}
    detail_points[source_box] = source_point
    detail_points[dest_box] = destination_point

    forward_distances = {}
    forward_distances[source_box] = 0

    forward_backpointers = {}
    forward_backpointers[source_point] = None

    backward_distances = {}
    backward_distances[dest_box] = 0

    backward_backpointers = {}
    backward_backpointers[dest_box] = None

    #boxes[source_box] = (None, source_point)

    while queue:                                        #djikstras
        current_dist, current_box, current_goal = heappop(queue)            
        if (current_goal == 'destination' and current_box in backward_distances):
            break
        elif (current_goal == 'source' and current_box in forward_distances):
            break
        else:
            for adj_box in mesh['adj'][current_box]:
                current_point = detail_points[current_box]
                adj_point = findDetailPoint(current_box, adj_box, current_box)
                if current_goal == 'destination':
                    pathcost = forward_distances[current_box] + euclidean(current_point, adj_point)
                    if adj_box not in forward_distances or pathcost < forward_distances[adj_box]:
                        detail_points[adj_box] = adj_point
                        forward_distances[adj_box] = pathcost
                        forward_backpointers[adj_box] = current_box
                        queue_dist = euclidean(adj_point, destination_point)
                        heappush(queue, (queue_dist, adj_box, current_goal))
                        boxes[adj_box] = current_box
                else:
                    pathcost = backward_distances[current_box] + euclidean(current_point, adj_point)
                    if adj_box not in backward_distances or pathcost < backward_distances[adj_box]:
                        detail_points[adj_box] = adj_point
                        backward_distances[adj_box] = pathcost
                        backward_backpointers[adj_box] = current_box
                        queue_dist = euclidean(adj_point, source_point)
                        heappush(queue, (queue_dist, adj_box, current_goal))
                        boxes[adj_box] = current_box
    
    midpoint = current_box
    ftb_box = midpoint
    btf_box = midpoint
    back_to_front = []
    while btf_box:
        if (btf_box == dest_box):
            back_to_front.append(destination_point)
            break
        back_to_front.append(detail_points[btf_box])
        btf_box = backward_backpointers[btf_box]
        if(btf_box):
            back_to_front.append(detail_points[btf_box])

    front_to_back = []
    while ftb_box:
        if (ftb_box == source_box):
            front_to_back.append(source_point)
            break
        front_to_back.append(detail_points[ftb_box])
        ftb_box = forward_backpointers[ftb_box]
        if(ftb_box):
            front_to_back.append(detail_points[ftb_box])

    
    list.reverse(back_to_front)
    path = back_to_front
    path.extend(front_to_back)
    return (path, boxes.keys())

def point_within_box(point, box):                       #check if a point is within a given box
    if box[0] <= point[0] and box[1] >= point[0] and box[2] <= point[1] and box[3] >= point[1]:
        return True
    else:
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

    detailPoint = [0,0]

    #print ("minx",minX, maxX, minY, maxY)
    #print ("o",originPoint)



    if minX == maxX: #vertical
        detailPoint[0] = minX
        #print("vertical")
        if (originPoint[1]) > minY:
            detailPoint[1] = minY
        elif (originPoint[1] < maxY):
            detailPoint[1] = maxY
        else:
            detailPoint[1] = originPoint[1]
        
    if minY == maxY: #horizontal
        detailPoint[1] = minY
        #print("horizontal")
        if (originPoint[0]) > minX:
            detailPoint[0] = minX
        elif (originPoint[0] < maxX):
            detailPoint[0] = maxX
        else:
            detailPoint[0] = originPoint[0]

    return detailPoint
def box_center(box):
    return ((box[0] + box[2])/2, (box[1] + box[3])/2)