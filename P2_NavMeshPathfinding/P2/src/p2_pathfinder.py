import queue

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

    while queue:                                        #breadth first search
        #current_node = bfsqueue.get()
        dist, current_box = headpop(queue)
        if(current_node == destination_point):
            print('gottem')
            #return path
        else:
            for adj_box in mesh['adj'][current_box]:
            #for new in mesh['adj'][current_node]:       #(haven't figured out how to do this part yet)
                #if new.prev == none
                    #new.prev = current_node
                    #push new to queue
                print()
    return path, boxes.keys()

def point_within_box(point, box):                       #check if a point is within a given box
    if box[0] < point[0] and box[1] > point[0] and box[2] < point[1] and box[3] > point[1]:
        return True
    else:
        return False

def box_of_point(mesh, point):
    for box in mesh['boxes']:                           #get the box for a given point
        if point_within_box(point, box):
            return box
    return False
