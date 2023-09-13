# Import necessary libraries
import json  # To work with JSON data
import matplotlib.pyplot as plt  # To visualize data
import networkx as nx  # To work with graphs
from networkx.drawing.nx_agraph import graphviz_layout  # To use Graphviz for layout

# Function to load JSON data from a file


def load_json_graph(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Recursive function to add edges and nodes to the graph from the JSON data


def add_edges(graph, node, parent=None):
    if parent is not None:
        graph.add_edge(parent, node['id'])
    graph.add_node(node['id'], label=node['label'], value=node.get('value', 0))
    for child in node.get('children', []):
        add_edges(graph, child, node['id'])

# Function to find and sum the values of all the ancestors of a node


def find_parent_values(graph, node):
    parents = nx.ancestors(graph, node)
    values = [graph.nodes[parent].get('value', 0) for parent in parents]
    return sum(values)

# Function to visualize the graph (referred to as "attack tree")


def visualize_attack_tree(json_graph):
    graph = nx.DiGraph()  # Create a directed graph

    # Add root node to the graph
    root_node = json_graph
    graph.add_node(root_node['id'], label=root_node['label'],
                   value=root_node.get('value', 0))
    add_edges(graph, root_node)  # Add edges and other nodes recursively

    # Set up graph layout
    pos = graphviz_layout(graph, prog="dot")
    # Set up labels with node label and value
    labels = {
        node: f"{graph.nodes[node]['label']} ({graph.nodes[node].get('value', '')})" for node in graph.nodes()}
    index_to_node = {i: node for i, node in enumerate(graph.nodes)}

    # Function to update labels (used after modifying node values interactively)
    def update_labels():
        nonlocal labels
        labels = {
            node: f"{graph.nodes[node]['label']} ({graph.nodes[node].get('value', '')})" for node in graph.nodes()}

    # Event handler function for clicking on nodes
    def on_pick(event):
        node_idx = index_to_node[event.ind[0]]
        node_attrs = graph.nodes[node_idx]

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
        plt.clf()
        nx.draw(graph, pos, with_labels=False,
                node_size=1000, node_color='skyblue')
        nx.draw_networkx_labels(graph, pos, labels=labels)
        for i, (node, (x, y)) in enumerate(pos.items()):
            plt.scatter(x, y, s=1000, c='skyblue', picker=True)
        plt.draw()

    # Set up figure and connect event handler
    fig = plt.figure()
    fig.canvas.mpl_connect('pick_event', on_pick)

    # Initial drawing of the graph
    nx.draw(graph, pos, with_labels=False,
            node_size=1000, node_color='skyblue')
    nx.draw_networkx_labels(graph, pos, labels=labels)
    for i, (node, (x, y)) in enumerate(pos.items()):
        plt.scatter(x, y, s=1000, c='skyblue', picker=True)
    plt.show()

# Function to sum individual paths recursively


def sum_routes(json_path):
    def recursive_sum(node, current_sum, current_path, results):
        current_sum += node['value']
        current_path.append(node['label'])

        # If node has children, continue recursion, else append results
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
    with open(json_path, 'r') as f:
        data = json.load(f)

    results = []
    recursive_sum(data, 0, [], results)

    # Print the individual route sums
    for res in results:
        print(
            f"Leaf Node: {res['leaf_label']}, Path: {res['path_labels']}, Sum: {res['sum']}")


# Main script execution
if __name__ == "__main__":
    # Specify the JSON file path
    filename = "./tree.json"

    # Execute both sum_routes and visualize_attack_tree functions
    sum_routes(filename)
    json_graph = load_json_graph(filename)
    visualize_attack_tree(json_graph)
