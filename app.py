import json
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout


def load_json_graph(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def add_edges(graph, node, parent=None):
    if parent is not None:
        graph.add_edge(parent, node['id'])
    graph.add_node(node['id'], label=node['label'], value=node.get('value', 0))
    for child in node.get('children', []):
        add_edges(graph, child, node['id'])


def find_parent_values(graph, node):
    parents = nx.ancestors(graph, node)
    values = [graph.nodes[parent].get('value', 0) for parent in parents]
    return sum(values)


def visualize_attack_tree(json_graph):
    graph = nx.DiGraph()

    root_node = json_graph
    graph.add_node(root_node['id'], label=root_node['label'],
                   value=root_node.get('value', 0))
    add_edges(graph, root_node)

    pos = graphviz_layout(graph, prog="dot")
    labels = {
        node: f"{graph.nodes[node]['label']} ({graph.nodes[node].get('value', '')})" for node in graph.nodes()}
    index_to_node = {i: node for i, node in enumerate(graph.nodes)}

    def update_labels():
        nonlocal labels
        labels = {
            node: f"{graph.nodes[node]['label']} ({graph.nodes[node].get('value', '')})" for node in graph.nodes()}

    def on_pick(event):
        node_idx = index_to_node[event.ind[0]]
        print(event.artist)

        node_attrs = graph.nodes[node_idx]

        parent_sum = find_parent_values(graph, node_idx)

        value = input(
            f"Provide a value for node {node_attrs['label']}, sum of parent values: {parent_sum}: ")
        try:
            value = float(value)
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        node_attrs['value'] = value
        print(f"Set value of node {node_attrs['label']} to {value}")

        update_labels()
        plt.clf()
        nx.draw(graph, pos, with_labels=False,
                node_size=1000, node_color='skyblue')
        nx.draw_networkx_labels(graph, pos, labels=labels)
        for i, (node, (x, y)) in enumerate(pos.items()):
            plt.scatter(x, y, s=1000, c='skyblue', picker=True)
        plt.draw()

    fig = plt.figure()
    fig.canvas.mpl_connect('pick_event', on_pick)

    nx.draw(graph, pos, with_labels=False,
            node_size=1000, node_color='skyblue')
    nx.draw_networkx_labels(graph, pos, labels=labels)
    for i, (node, (x, y)) in enumerate(pos.items()):
        plt.scatter(x, y, s=1000, c='skyblue', picker=True)

    plt.show()


if __name__ == "__main__":
    # Replace with the path to your JSON file
    filename = "./tree.json"
    json_graph = load_json_graph(filename)
    visualize_attack_tree(json_graph)
