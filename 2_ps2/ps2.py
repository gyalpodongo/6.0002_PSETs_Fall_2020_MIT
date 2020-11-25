# 6.0002 Problem Set 2 Fall 2020
# Graph Optimization
# Name: Gyalpo M. Dongo Aguirre
# Collaborators: Rabab A Alrufayi
# Time: 3:00

#
# Finding shortest paths to drive from home to work on a road network
#

from graph import DirectedRoad, Node, RoadMap


# PROBLEM 2: Building the Road Network
#
# PROBLEM 2a: Designing your Graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the times
# represented?
#Node = Nodes of Graph
#DirectedRoad = Edges of Graph
#Time = Weight


# PROBLEM 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a road map (graph).

    Parameters:
        map_filename : String
            name of the map file

    Assumes:
        Each entry in the map file consists of the following format, separated by spaces:
            src_node dest_node travel_time road_type

        Note: mountain road types always are uphill in the source to destination direction and
              downhill in the destination to the source direction. Downhill travel takes
              half as long as uphill travel. The travel_time represents the time to travel 
              from source to destination (uphill).

        e.g.
            N0 N1 10 interstate
        This entry would become two directed roads; one from 'N0' to 'N1' on an interstate highway with 
        a weight of 10, and another road from 'N1' to 'N0' on an interstate using the same weight.

        e.g. 
            N2 N3 7 mountain 
        This entry would become to directed roads; one from 'N2' to 'N3' on a mountain road with 
        a weight of 7, and another road from 'N3' to 'N2' on a mountain road with a weight of 3.5.

    Returns:
        a directed road map representing the inputted map
    """
    map_file = open(map_filename)
    road_map = RoadMap()
    for line in map_file:
        node1 = Node(line.split()[0])
        node2 = Node(line.split()[1])
        time = float(line.split()[2])
        road_type = line.split()[3]
        #As the map will contain roads going on both ways, road1 will be the
        #road going from node 1 to node 2 and road 2 will be the opposite.
        road1 = DirectedRoad(node1,node2,time,road_type)
        if road_type == 'mountain':
            time = time/2
        road2 = DirectedRoad(node2,node1,time,road_type)
        if not road_map.contains_node(node1):
            road_map.insert_node(node1)
        if not road_map.contains_node(node2):
            road_map.insert_node(node2)
        road_map.insert_road(road1)
        road_map.insert_road(road2)  
    return road_map
# PROBLEM 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out after testing


#road_map = load_map("maps/test_load_map.txt")
#print(road_map)


# PROBLEM 3: Finding the Shortest Path using Optimized Search Method



# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer: Being able to find the shortest weighted path between one node to 
# another using Dijkstra’s Algorithm.


# PROBLEM 3b: Implement find_optimal_path
def find_optimal_path(roadmap, start, end, restricted_roads, has_traffic=False):
    """
    Finds the shortest path between nodes subject to constraints.

    Parameters:
    roadmap - RoadMap
        The graph on which to carry out the search
    start - Node
        node at which to start
    end - Node
        node at which to end
    restricted_roads - list[strings]
        Road Types not allowed on path
    has_traffic - boolean
        flag to indicate whether to get shortest path during heavy or normal traffic 

    Returns:
    A tuple of the form (best_path, best_time).
        The first item is the shortest-path from start to end, represented by
        a list of nodes (Nodes).
        The second item is an number(float), the length (time traveled)
        of the best path.

    If there exists no path that satisfies constraints, then return None.
    """
    if not (roadmap.contains_node(start) and roadmap.contains_node(end)):
        #This is because if map doesn't contian one of the nodes, the path
        #doesn't exist
        return None
    else: 
        if start == end:
            path = [start]
            time = 0.0
        else:
            unvisited = list(roadmap.get_all_nodes())
            #timeTo is a dictionnary which will end up showing how long it will
            #take to one node from the starting node
            timeTo = {node: float('inf') for node in unvisited}
            timeTo[start] = 0
            predecessor = {node: None for node in unvisited}
            while len(unvisited) != 0:
                current = min(unvisited, key=lambda node: timeTo[node])
                if timeTo[current] == float('inf'):
                    break
                #this will create a list of the neighbour nodes which are
                #subject to the restricted types of roads
                reachable_neighbours = roadmap.get_reachable_neighbors(current,restricted_roads)
                for road in roadmap.get_roads_starting_at_node(current):
                    alternativePathTime = timeTo[current] + road.get_travel_time(has_traffic)
                    neighbour = road.get_destination_node()
                    if neighbour in reachable_neighbours:
                        if alternativePathTime < timeTo[neighbour]:
                            timeTo[neighbour] = alternativePathTime
                            predecessor[neighbour] = current
                unvisited.remove(current)
            path = []
            current = end
            time = timeTo[end]
            while predecessor[current] != None:
                path.insert(0, current)
                current = predecessor[current]
            if path != []:
                path.insert(0, current)
            else:
                path = None
        if path != None:
            return(path,time)
        else:
            return None
# PROBLEM 4a: Implement optimal_path_no_traffic
def optimal_path_no_traffic(filename, start, end):
    """
    Finds the shortest path from start to end during ideal traffic conditions.

    You must use find_optimal_path and load_map.

    Parameters:
    filename - name of the map file that contains the graph
    start - Node, node object at which to start
    end - Node, node object at which to end
    
    Returns:
    list of Node objects, the shortest path from start to end in normal traffic.
    If there exists no path, then return None.
    """
    road_map = load_map(filename)
    restricted_roads = []
    if find_optimal_path(road_map,start,end,restricted_roads) != None:
        return find_optimal_path(road_map,start,end,restricted_roads)[0]
    else:
        return None
    

# PROBLEM 4b: Implement optimal_path_restricted
def optimal_path_restricted(filename, start, end):
    """
    Finds the shortest path from start to end when local roads and mountain roads cannot be used.

    You must use find_optimal_path and load_map.

    Parameters:
    filename - name of the map file that contains the graph
    start - Node, node object at which to start
    end - Node, node object at which to end
    
    Returns:
    list of Node objects, the shortest path from start to end given the aforementioned conditions,
    If there exists no path that satisfies constraints, then return None.
    """
    road_map = load_map(filename)
    restricted_roads = ['local','mountain']
    if find_optimal_path(road_map,start,end,restricted_roads) != None:
        return find_optimal_path(road_map,start,end,restricted_roads)[0]
    else:
        return None
    

# PROBLEM 4c: Implement optimal_path_heavy_traffic
def optimal_path_heavy_traffic(filename, start, end):
    """
    Finds the shortest path from start to end in heavy traffic,
    i.e. when local roads take twice as long. 

    You must use find_optimal_path and load_map.

    Parameters:
    filename - name of the map file that contains the graph
    start - Node, node object at which to start
    end - Node, node object at which to end; you may assume that start != end
    
    Returns:
    The shortest path from start to end given the aforementioned conditions, 
    represented by a list of nodes (Nodes).

    If there exists no path that satisfies the constraints, then return None.
    """
    road_map = load_map(filename)
    restricted_roads = []
    has_traffic = True
    if find_optimal_path(road_map,start,end,restricted_roads,has_traffic) != None:
        return find_optimal_path(road_map,start,end,restricted_roads,has_traffic)[0]
    else:
        return None
    
if __name__ == '__main__':
    # UNCOMMENT THE FOLLOWING LINES TO DEBUG
    pass
    rmap = load_map('maps/road_map.txt')
    start = Node('N0')
    end = Node('N9')
    restricted_roads = ['']
    #print(find_optimal_path(rmap, start, end, restricted_roads))
