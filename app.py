"""
This script visualizes a hierarchical tree structure described in a JSON file.
It uses matplotlib to visualize the tree and allows interactive updating of node values.
"""

# Import libraries
import json  # To work with JSON data
import matplotlib.pyplot as plt  # To visualize data using various plot types
import networkx as nx  # To create, manipulate, and study complex networks of nodes and edges
from networkx.drawing.nx_agraph import graphviz_layout  # To use Graphviz for better layout and visualization of the graph



# Recursive function to add edges and nodes to the graph from the JSON data
def add_edges(graph, node, parent=None):
    """
    Recursive function to add edges and nodes to the graph from the JSON data.

    Args:
    graph (networkx.DiGraph): The graph to which nodes and edges are being added.
    node (dict): The current node being processed.
    parent (str, optional): The parent of the current node. Defaults to None.
    """
   
    # For the first call (starting with the root node), parent is None. This is when the root node is added to the graph, but no edge is added because parent is None.
    if parent is not None:
        graph.add_edge(parent, node['id'])
    # Each node from the JSON data is added to the graph including its predefined id, label, and value
    graph.add_node(node['id'], label=node['label'], value=node.get('value', 0))
    # If the node has children, add edges (relationships between nodes) and nodes recursively, making the current node the parent
    for child in node.get('children', []):
        add_edges(graph, child, node['id'])

# Function to find and sum the values of all the ancestors of a node


def find_parent_values(graph, node):
    """
    Find and sum the values of all ancestors of a node.

    Args:
    graph (networkx.DiGraph): The graph being processed.
    node (str): The ID of the node whose ancestors' values are being summed.

    Returns:
    float: The sum of the values of all ancestor nodes.
    """
    parents = nx.ancestors(graph, node)
    # for each of the parent nodes of the selected node, find and sum all of the values
    values = [graph.nodes[parent].get('value', 0) for parent in parents]
    return sum(values)

# Function to visualize the graph (referred to as "attack tree")


def visualize_attack_tree(json_graph_data):
    """
    Visualize a hierarchical tree structure using NetworkX and Matplotlib.

    Args:
    json_graph_data (dict): The hierarchical data loaded from a JSON file.
    """
    graph = nx.DiGraph()  # Create a directed graph, the shape of an attack tree

    # Add nodes using recursive function
    add_edges(graph, json_graph_data)

    # Set up graph layout using graphviz dot layout https://graphviz.org/docs/layouts/dot/
    pos = graphviz_layout(graph, prog="dot")

    # Create dictionary of labels and node values for the graph
    labels = {
        node: f"{graph.nodes[node]['label']} ({graph.nodes[node].get('value', '')})" for node in graph.nodes()}

    # Create dictionary of nodes and their respective indices for updating later
    index_to_node = {i: node for i, node in enumerate(graph.nodes)}

    # Event handler function for clicking on nodes
    def on_pick(event):
        # Get node attributes and index when it is clicked so we can update the value
        node_idx = index_to_node[event.ind[0]]
        node_attrs = graph.nodes[node_idx]

        # Find and display the sum of all the parent node values
        parent_sum = find_parent_values(graph, node_idx)

        # Get new value input from the user
        value = input(
            f"Provide a value for node {node_attrs['label']}, sum of parent values: {parent_sum}: ")
        try:
            value = float(value)
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        # Update node value and print confirmation
        node_attrs['value'] = value
        print(f"Set value of node {node_attrs['label']} to {value}")

        # Update labels and redraw graph
        update_labels()
        redraw_graph(graph, pos, labels)

    # Function to update labels (used after modifying node values interactively)
    def update_labels():
        nonlocal labels
        labels = {
            node: f"{graph.nodes[node]['label']} ({graph.nodes[node].get('value', '')})" for node in graph.nodes()}

    # Set up figure and connect event handler
    fig = plt.figure()
    fig.canvas.mpl_connect('pick_event', on_pick)

    # Initial drawing of the graph
    draw_initial_graph(graph, pos, labels)


def redraw_graph(graph, pos, labels):
    """
    Redraw the graph with updated labels.

    Args:
    graph (networkx.DiGraph): The graph to be redrawn.
    pos (dict): The positions of the nodes.
    labels (dict): The labels of the nodes.
    """
    # Clear off existing graph, then redraw, then show
    plt.clf()
    draw_graph(graph, pos, labels)
    plt.draw()


def draw_initial_graph(graph, pos, labels):
    """
    Initially draw the graph using Matplotlib.

    Args:
    graph (networkx.DiGraph): The graph to be drawn initially.
    pos (dict): The positions of the nodes.
    labels (dict): The labels of the nodes.
    """
    draw_graph(graph, pos, labels)
    plt.show()


def draw_graph(graph, pos, labels):
    """
    Draw the graph with given node positions and labels.

    Args:
    graph (networkx.DiGraph): The graph to be drawn.
    pos (dict): The positions of the nodes.
    labels (dict): The labels of the nodes.
    """
    # Draw new graph with updated information using the plt draw function
    # Graph nodes are drawn  followed by labels
    nx.draw(graph, pos,
            node_size=1000, node_color='skyblue')
    nx.draw_networkx_labels(graph, pos, labels=labels)
    for i, (node, (x, y)) in enumerate(pos.items()):
        plt.scatter(x, y, s=1000, c='skyblue', picker=True)

# Function to sum individual paths recursively to show user in the following format:
# Leaf Node: Blackmail, Path: Data Breach -> Insider Threat -> Bribery -> Blackmail, Sum: 1305000

def sum_routes(json_graph):
    """
    Sum individual paths recursively and display each path with corresponding sum to the user.

    Args:
    json_graph (dict): The hierarchical data loaded from a JSON file.
    """
    def recursive_sum(node, current_sum, current_path, results):
        current_sum += node['value']
        current_path.append(node['label'])

        # If node has children, continue recursion, else append results to the path that is being built
        if 'children' in node:
            for child in node['children']:
                recursive_sum(child, current_sum, current_path.copy(), results)
        else:
            results.append({
                'leaf_label': node['label'],
                'path_labels': ' -> '.join(current_path),
                'sum': current_sum
            })

    # Load JSON data and initiate recursion

    results = []
    recursive_sum(json_graph, 0, [], results)

    # Print the individual route sums and return the results for testing
    for res in results:
        print(
            f"Leaf Node: {res['leaf_label']}, Path: {res['path_labels']}, Sum: {res['sum']}")
    return results

# Main script execution
if __name__ == "__main__":
    # Specify the JSON file path
    # filename = "./digitization_challenges.json"
    # filename = "./local_supplier_issues.json"
    filename = "./data_breach.json"

    # Execute both sum_routes and visualize_attack_tree functions

    json_graph = json.load(open(filename))
    sum_routes(json_graph)
    visualize_attack_tree(json_graph)
