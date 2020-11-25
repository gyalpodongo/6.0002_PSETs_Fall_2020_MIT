#!/usr/bin/env python

from graph import Node, DirectedRoad, RoadMap
from ps2 import load_map, find_optimal_path, optimal_path_no_traffic, optimal_path_heavy_traffic, optimal_path_restricted
import unittest


class InternalPs2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = RoadMap()
        cls.na = Node('NA')
        cls.nb = Node('NB')
        cls.nc = Node('NC')

        # for best path tests
        cls.n0 = Node('N0')
        cls.n1 = Node('N1')
        cls.n2 = Node('N2')
        cls.n3 = Node('N3')
        cls.n4 = Node('N4')
        cls.n5 = Node('N5')
        cls.n6 = Node('N6')
        cls.n7 = Node('N7')
        cls.n8 = Node('N8')
        cls.n9 = Node('N9')
        cls.n10 = Node('N10')

        cls.m.insert_node(cls.na)
        cls.m.insert_node(cls.nb)
        cls.m.insert_node(cls.nc)
        cls.r1 = DirectedRoad(cls.na, cls.nb, 5, 'local')
        cls.r2 = DirectedRoad(cls.na, cls.nc, 10, 'mountain')
        cls.r3 = DirectedRoad(cls.nb, cls.nc, 18, 'interstate')
        cls.r4 = DirectedRoad(cls.n2, cls.n4, 3.5, 'mountain')

        cls.m.insert_road(cls.r1)
        cls.m.insert_road(cls.r2)
        cls.m.insert_road(cls.r3)
        cls.road_map = load_map("maps/road_map.txt")

    # ------------------------------------------------ testing graph.py

    ## testing DirectedRoad
    def test_1_graph_weighted_edge_src(self):
        self.assertEqual(str(self.r1.get_source_node()), str(self.na), "your DirectedRoad get_source_node() method is failing.")
        self.assertEqual(str(self.r2.get_source_node()), str(self.na), "your DirectedRoad get_source_node() method is failing.")
        self.assertEqual(str(self.r3.get_source_node()), str(self.nb), "your DirectedRoad get_source_node() method is failing.")

    def test_1_graph_weighted_edge_dest(self):
        self.assertEqual(str(self.r1.get_destination_node()), str(self.nb), "your DirectedRoad get_destination_node() method is failing.")
        self.assertEqual(str(self.r2.get_destination_node()), str(self.nc), "your DirectedRoad get_destination_node() method is failing.")
        self.assertEqual(str(self.r3.get_destination_node()), str(self.nc), "your DirectedRoad get_destination_node() method is failing.")

    def test_1_graph_weighted_edge_type(self):
        self.assertEqual(str(self.r1.get_road_type()), 'local', "your DirectedRoad get_road_type() method is failing.")
        self.assertEqual(str(self.r2.get_road_type()), 'mountain', "your DirectedRoad get_road_type() method is failing.")
        self.assertEqual(str(self.r3.get_road_type()), 'interstate', "your DirectedRoad get_road_type() method is failing.")

    def test_1_graph_weighted_edge_total_time(self):
        self.assertEqual(self.r1.get_travel_time(), 5, "your DirectedRoad get_travel_time() method is failing, in no traffic.")
        self.assertEqual(self.r2.get_travel_time(), 10, "your DirectedRoad get_travel_time() method is failing, in no traffic.")
        self.assertEqual(self.r3.get_travel_time(), 18, "your DirectedRoad get_travel_time() method is failing, in no traffic.")
        self.assertEqual(self.r1.get_travel_time(has_traffic=True), 10, "your DirectedRoad get_travel_time() method is failing, in traffic for local road.")
        self.assertEqual(self.r2.get_travel_time(has_traffic=True), 10, "your DirectedRoad get_travel_time() method is failing, in traffic for mountain road.")
        self.assertEqual(self.r3.get_travel_time(has_traffic=True), 18, "your DirectedRoad get_travel_time() method is failing, in traffic for interstate road.")
    
    def test_1_graph_weighted_edge_str(self):
        self.assertEqual(str(self.r1), "NA -> NB takes 5 minute(s) via local road", "your DirectedRoad __str__() method is failing.")
        self.assertEqual(str(self.r2), "NA -> NC takes 10 minute(s) via mountain road", "your DirectedRoad __str__() method is failing.")
        self.assertEqual(str(self.r3), "NB -> NC takes 18 minute(s) via interstate road", "your DirectedRoad __str__() method is failing.")

    
    ## testing RoadMap 
    def test_1_graph_insert_node(self): 
        self.assertTrue(self.m.contains_node(self.nc), msg="Either your RoadMap insert_node() or contains_node() method are failing")

    def test_1_graph_insert_existing_node_raises(self):
        with self.assertRaises(ValueError, msg="your RoadMap insert_node() method doesn't raise ValueError when adding existing node to the map"):
            self.m.insert_node(self.na)

    def test_1_graph_get_all_nodes(self):
        self.assertEqual(self.m.get_all_nodes(), set([self.na,self.nb, self.nc]), "Your RoadMap get_all_nodes() method doesn't return the correct nodes")
        # TODO: test they are returning a copy not the actual set  
    
    def test_1_graph_insert_road(self):
        self.assertEqual(self.m.get_roads_starting_at_node(self.na), [self.r1, self.r2], "Your RoadMap get_roads_starting_at_node() method doesn't return the correct roads")
        self.assertEqual(self.m.get_roads_starting_at_node(self.n0),[], "Your RoadMap get_roads_starting_at_node() method doesn't return [] when node is not in map")

    def test_1_graph_insert_road_to_nonexistent_node_raises(self):
        node_not_in_graph = Node('SC')
        no_src = DirectedRoad(self.nb, node_not_in_graph, 9, 'bridge')
        no_dest = DirectedRoad(node_not_in_graph, self.na, 9, 'bridge')

        with self.assertRaises(ValueError, msg="your RoadMap insert_road() method doesn't raise ValueError when adding road whose source is not in the map"):
            self.m.insert_road(no_src)
        with self.assertRaises(ValueError, msg="your RoadMap insert_road() method doesn't raise ValueError when adding road whose destination is not in the map"):
            self.m.insert_road(no_dest)

    def test_1_graph_str(self):
        lines = ["NA -> NB takes 5 minute(s) via local road", 
                 "NA -> NC takes 10 minute(s) via mountain road",
                 "NB -> NC takes 18 minute(s) via interstate road"]
        actual = str(self.m).split("\n")
        self.assertIn(
            lines[0], actual, "Your printed graph does not match the correct string")
        self.assertIn(
            lines[1], actual, "Your printed graph does not match the correct string")
        self.assertIn(
            lines[2], actual, "Your printed graph does not match the correct string")

    # ------------------------------------------------ testing ps2.py

    def test_2_load_map(self):
        self.assertTrue(isinstance(self.road_map, RoadMap))
        self.assertEqual(len(self.road_map.nodes), 10)
        all_roads = []
        for _, roads in self.road_map.nodes_to_roads.items():
            all_roads += roads  # edges must be dict of node -> list of edges
            for road in roads:
                self.assertFalse('\n' in road.get_road_type(),
                                 "Your road type contains a new line character. Check the reading/parsing in load_map")
        all_roads = set(all_roads)
        self.assertIn(str(self.r4), [str(i) for i in all_roads])
        self.assertEqual(len(all_roads), 26)

    def _print_path_description(self, start, end, restricted_roads):
        constraint = ""
        if restricted_roads != []:
            constraint += " and without using the {} line(s)".format(
                restricted_roads)
        #print("------------------------")
        #print("Shortest path from Node {} to {} {}".format(
        #    start, end, constraint))

    def _test_path(self, graph, expectedPath, expectedTime, message="", restricted_roads=[]):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, restricted_roads)
        student_path = find_optimal_path(graph, start, end, restricted_roads)
        #print("(Expected Path, Expected Time): ", (expectedPath, expectedTime))
        #print("(Your Path, Your Time): ", student_path)
        self.assertEqual(student_path[0], expectedPath, message)
        self.assertEqual(student_path[1], expectedTime,
                         "Time incorrect: " + message)

    def _test_impossible_path(self, graph,
                              start,
                              end,
                              restricted_roads=[], message=""):

        self._print_path_description(start, end, restricted_roads)
        student_path = find_optimal_path(graph, start, end, restricted_roads)
        self.assertEqual(student_path, None, message)

    def test_3_map1_path_one_step(self):
        self._test_path(self.road_map, expectedPath=[self.n0, self.n1], expectedTime=15,
                        message="The path goes one step. Make sure you are looking at all of the neighboring nodes.")

    def test_3_map2_path_limited_time(self):
        self._test_path(self.road_map,
                        expectedPath=[self.n0, self.n2, self.n4, self.n5], expectedTime=14.5, message="Make sure your algorithm is finding the shortest path.")

    def test_3_map3_path_restricted_path(self):
        self._test_path(self.road_map, expectedPath=[self.n0, self.n2, self.n3], expectedTime=16, restricted_roads=[
                        'interstate'], message="The path tests having a restricted list of road types. Make sure your algorithm is finding the shortest correct path.")

    def test_3_map_path_start_end_same(self):
        student_path = find_optimal_path(self.road_map, self.n1, self.n1, [])
        self.assertEqual(student_path[0], [self.n1], "If the start and end are the same, the path should be the start node")
        self.assertEqual(
            student_path[1], 0, "If the start and end are the same, the time traveled should be zero")

    def test_3_map_path_same_length_different_time(self):
        self._test_path(self.road_map, expectedPath=[self.n0, self.n2, self.n3, self.n6], expectedTime=21,
                        message="Should find path that has the shortest length of all edges combined")

    def test_3_path_multiple_roads_not_allowed(self):
        self._test_path(self.road_map, expectedPath=[self.n0, self.n1, self.n3, self.n8, self.n9], expectedTime=46, restricted_roads=[
                        'mountain', 'local'], message="Make sure your search works with multiple restricted roads")

    def test_3_impossible_path_no_interstate(self):
        self._test_impossible_path(self.road_map, start=self.n0, end=self.n10, restricted_roads=[
                                   'interstate'], message="Should be impossible")

    def test_3_impossible_path_no_interstate_no_local(self):
        self._test_impossible_path(self.road_map, start=self.n1, end=self.n9, restricted_roads=[
                                   'interstate', 'local'], message="Should be impossible")

    def test_3_map_traverse_mountain(self):
        self._test_path(self.road_map, expectedPath=[self.n0, self.n2, self.n3], expectedTime=16,
                        message="The path has two edges. Make sure you are looking at all of the neighboring nodes.")
    

    def test_4a_optimal_path_no_traffic(self):
        expected_path, results = [Node('N0'), Node('N2'), Node('N3'), Node('N6'), Node('N8'), Node('N9')], optimal_path_no_traffic("maps/road_map.txt", Node('N0'), Node('N9'))
        self.assertEqual(list, type(results), "Make sure you are returning the correct type")
        self.assertEqual(expected_path, results, "Make sure your optimal_path_no_traffic is correct")

    def test_4b_optimal_path_restricted_avoid_local(self):
        expected_path, results = [Node('N3'), Node('N8'), Node('N7'), Node('N6')], optimal_path_restricted("maps/road_map.txt", Node('N3'), Node('N6'))
        self.assertEqual(list, type(results), "Make sure you are returning the correct type")
        self.assertEqual(expected_path, results, "Make sure your optimal_path_restricted is correct")
        
    def test_4b_optimal_path_restricted_avoid_mountain(self):
        expected_path, results = [Node('N0'), Node('N1'), Node('N3') ], optimal_path_restricted("maps/road_map.txt", Node('N0'), Node('N3'))
        self.assertEqual(list, type(results), "Make sure you are returning the correct type")
        self.assertEqual(expected_path, results, "Make sure your optimal_path_restricted is correct")
        
    def test_4b_optimal_path_restricted_avoid_both_local_mountain(self):
        expected_path, results = [Node('N4'), Node('N5'), Node('N6'), Node('N7'), Node('N8'), Node('N3'), Node('N1'), Node('N0') ], optimal_path_restricted("maps/road_map.txt", Node('N4'), Node('N0'))
        self.assertEqual(list, type(results), "Make sure you are returning the correct type")
        self.assertEqual(expected_path, results, "Make sure your optimal_path_restricted is correct")
        

    def test_4c_optimal_path_heavy_traffic(self):
        expected_path, results = [Node('N0'), Node('N2'), Node('N3'), Node('N8'), Node('N9')], optimal_path_heavy_traffic("maps/road_map.txt", Node('N0'), Node('N9'))
        self.assertEqual(list, type(results), "Make sure you are returning the correct type")
        self.assertEqual(expected_path, results, "Make sure your optimal_path_heavy_traffic is correct")
       

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(InternalPs2Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
