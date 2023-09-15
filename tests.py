
import unittest
import networkx as nx
# Assuming your script name is tree_visualizer.py
from app import add_edges, find_parent_values, sum_routes

class TestTreeVisualizer(unittest.TestCase):

    def test_add_edges(self):
        graph = nx.DiGraph()
        node_data = {
            "id": "1",
            "label": "Root",
            "children": [
                {"id": "1.1", "label": "Child1"},
                {"id": "1.2", "label": "Child2"}
            ]
        }
        add_edges(graph, node_data)
        
        self.assertEqual(len(graph.nodes), 3)  # Check if 3 nodes are added
        self.assertEqual(len(graph.edges), 2)  # Check if 2 edges are created
        self.assertIn("1", graph.nodes)  # Check if root node is added
        self.assertIn("1.1", graph.nodes)  # Check if Child1 node is added
        self.assertIn("1.2", graph.nodes)  # Check if Child2 node is added

    def test_find_parent_values(self):
        graph = nx.DiGraph()
        graph.add_node('1', value=1)
        graph.add_node('1.1', value=2)
        graph.add_node('1.2', value=3)
        graph.add_edge('1', '1.1')
        graph.add_edge('1', '1.2')
        
        self.assertEqual(find_parent_values(graph, '1.1'), 1)  # Check if it returns the correct sum of parent values
        self.assertEqual(find_parent_values(graph, '1.2'), 1)  # Check if it returns the correct sum of parent values

    def test_sum_routes(self):
        json_graph_data = {
            "id": "1",
            "label": "Root",
            "value": 1,
            "children": [
                {"id": "1.1", "label": "Child1", "value": 2},
                {"id": "1.2", "label": "Child2", "value": 3}
            ]
        }
        result = [
            {'leaf_label': 'Child1', 'path_labels': 'Root -> Child1', 'sum': 3},
            {'leaf_label': 'Child2', 'path_labels': 'Root -> Child2', 'sum': 4}
        ]

        self.assertEqual(sum_routes(json_graph_data), result)  # Check if it returns the correct paths and sums

if __name__ == "__main__":
    unittest.main()
