# 6.0002 Problem Set 2 Fall 2020
# Graph Optimization
# Name: Gyalpo M. Dongo Aguirre
# Collaborators: Rabab A Alrufayi
# Time: 1:00


# This file contains a set of data structures to represent the graphs
# that you will be using for this pset.

class Node():
    """Represents a node in the graph"""

    def __init__(self, name):
        """
        Initializes  an instance of Node object.

        Parameters:
        name - object representing the name of the node
        """
        self.name = str(name)

    def get_name(self):
        """
        Returns:
        str, representing the name of the node
        """
        return self.name

    def __str__(self):
        """
        This is the function that is called when print(node) is called.

        Returns:
        str, humanly readable reprsentation of the node
        """
        return self.name

    def __repr__(self):
        """
        Formal string representation of the node

        Returns:
        str, the name of the node.
        """
        return self.name

    def __eq__(self, other):
        """
        This is function called when you use the "==" operator on nodes

        Parameters:
        other - Node object to compare against

        Returns:
        bool, True is self == other, false otherwise
        """
        if not isinstance(other, Node):
            return False
        return self.name == other.name

    def __ne__(self, other):
        """
        This is function called when you used the "!=" operator on nodes

        Parameters:
        other - Node object to compare against

        Returns:
        bool, True is self != other, false otherwise
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        Returns:
        Hash of the node. This function is necessary so that Nodes can be
        used as keys in a dictionary, Nodes are immutable
        """
        return self.name.__hash__()


# PROBLEM 1: Implement this class based on the given docstring.
class DirectedRoad():
    """Represents a road (edge) with a travel time (weight)"""

    def __init__(self, src_node, dest_node, travel_time, road_type):
        """
        Initialize src, dest, travel_time, and road_type for the DirectedRoad class

        Parameters:
        src: Node, representing the source node
        dest: Node, representing the destination node
        travel_time: float, representing the time travelled between the src and dest
        road_type: str, representing the type of road of the edge
        """
        self.src = src_node
        self.dest = dest_node
        self.travel_time = travel_time
        self.road_type = road_type

    def get_source_node(self):
        """
        Getter method for DirectedRoad

        Returns:
        Node, representing the source node
        """
        return self.src

    def get_destination_node(self):
        """
        Getter method for DirectedRoad

        Returns:
        Node, representing the destination node
        """
        return self.dest

    def get_road_type(self):
        """
        Getter method for DirectedRoad

        Returns:
        str, representing the road type of the road
        """
        return self.road_type

    def get_travel_time(self, has_traffic = False):
        """
        Gets the travel_time for this road. In traffic conditions:
        - all the local roads take twice as long.
        - all other road types take the same amount of time

        Paramater:
        has_traffic - bool, True if there is traffic, False otherwise

        Returns:
        float, representing the time travelled between the source and dest nodes
        """
        if has_traffic == True:
            if self.get_road_type() == 'local':
                return 2*self.travel_time
            else:
                return self.travel_time
        else:
            return self.travel_time



    def __str__(self):
        """
        Function that is called when print() is called on a DirectedRoad object.

        Returns:
        str, with the format 'src -> dest takes travel_time minute(s) via road_type road'

        Note: For the total time assume normal traffic conditions
        """
        statement = "{} -> {} takes {} minute(s) via {} road".format(self.get_source_node().get_name(),self.get_destination_node().get_name(),self.get_travel_time(),self.get_road_type())
        return statement

    def __hash__(self):
        return self.__str__().__hash__()

# PROBLEM 1: Implement methods of this class based on the given docstring.
# DO NOT CHANGE THE FUNCTIONS THAT HAVE BEEN IMPLEMENTED FOR YOU.
class RoadMap():
    """Represents a road map -> a directed graph of Node and DirectedRoad objects"""

    def __init__(self):
        """
        Initalizes a new instance of RoadMap.
        """
        self.nodes = set()
        self.nodes_to_roads = {}  # must be a dictionary of Node -> list of roads starting at that node

    def __str__(self):
        """
        Function that is called when print() is called on a RoadMap object.

        Returns:
        str, representation of the RoadMap.
        """
        road_strs = []
        for roads in self.nodes_to_roads.values():
            for road in roads:
                road_strs.append(str(road))
        road_strs = sorted(road_strs)  # sort alphabetically
        return '\n'.join(road_strs)  # concat road_strs with "\n"s between them

    def get_roads_starting_at_node(self, node):
        """
        Param:
        node object

        Return:
        a copy of the list of all of the roads that start at given node.
        empty list if the node is not in the graph
        """
        if node in self.nodes_to_roads.keys():
            return self.nodes_to_roads[node]
        else:
            return []

    def get_all_nodes(self):
        """
        Return:
        a COPY of all nodes in the RoadMap. Does not modify self.nodes
        """
        return self.nodes.copy()

    def contains_node(self, node):
        """
        Param:
        node object

        Return:
        True, if node is in the graph. False, otherwise.
        """
        return node in self.get_all_nodes()

    def insert_node(self, node):
        """
        Adds a Node object to the RoadMap.
        Raises a ValueError if it is already in the graph.

        Param:
        node object
        """
        if self.contains_node(node):
            raise ValueError("Node is already in the graph")
        else:
            self.nodes.add(node)
            self.nodes_to_roads[node] = []
            

    def insert_road(self, road):
        """
        Adds a DirectedRoad instance to the RoadMap.
        Raises a ValueError if either of the nodes associated with the road is not in the graph.

        Param:
        road, DirectedRoad object
        """
        if self.contains_node(road.get_source_node()) and self.contains_node(road.get_destination_node()):
            self.nodes_to_roads[road.src].append(road)
        else:
            if not (self.contains_node(road.get_source_node()) and self.contains_node(road.get_destination_node())):
                raise ValueError("Neither of the nddes associated with the road are in the graph.")
            elif self.contains_node(road.src):
                raise ValueError("Destination node of road is not in the graph")
            else:
                raise ValueError("Source node of road is not in the graph")
            
                

    def get_reachable_neighbors(self, node, restricted_roads=[]):
        """
        Finds the neighbors of a node in a given roadmap that can be reached
        without considering roads of type in restricted_roads.

        Param:
        node - Node object, whose neighbors to retrieve
        restricted_roads: list of str, road types not under consideration

        Returns:
        list of nodes that neighbour the given node and aren't of the restricted type.
        """
        node_roads = self.get_roads_starting_at_node(node)
        neighbour_nodes = []
        for road in node_roads:
            if road.get_road_type() not in restricted_roads:
                neighbour_nodes.append(road.get_destination_node())
        return neighbour_nodes
       
        
                
