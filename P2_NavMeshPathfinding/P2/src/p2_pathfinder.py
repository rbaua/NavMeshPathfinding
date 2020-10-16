
def find_path (source_point, destination_point, mesh):

    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """

    path = []
    boxes = {}
    for box in mesh['boxes']:
        #print(box, 'box')
        if box[0] < source_point[0] and box[1] > source_point[0] and box[2] < source_point[1] and box[3] > source_point[1]:
            print('found source point')
        if box[0] < destination_point[0] and box[1] > destination_point[0] and box[2] < destination_point[1] and box[3] > destination_point[1]:
            print('found destination point')
    print(mesh['adj'])
    return path, boxes.keys()
