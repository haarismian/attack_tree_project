import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from matplotlib.collections import PatchCollection

def on_pick(event):
#     graph = event.artist.graph
#     eventnode = event.nodes
    eventartist = event.artist
    print(eventartist)
    print(eventartist.get_url())
    print(event.artist.id)
    for i in event.ind:
            # color = event.artist.get_facecolor()[i]
            print(i)


if __name__ == "__main__":
    # Specify the JSON file path
    # filename = "./digitization_challenges.json"
    # filename = "./local_supplier_issues.json"
    filename = "./data_breach.json"

    # # Execute both sum_routes and visualize_attack_tree functions
    # json_graph = load_json_graph(filename)
    # visualize_attack_tree(json_graph)

    graph = nx.DiGraph()  # Create a directed graph
    graph.add_node(1)
    graph.add_node(8, time="5pm")
    graph.add_edge(1,2)
    graph.add_edge(2,3)
    graph.add_edge(1,4)
    graph.add_node(3)  # Add node 1
    fig = plt.figure()
    fig.canvas.mpl_connect('pick_event', on_pick)

    pos = graphviz_layout(graph, prog="dot")
    nx.draw(graph, pos, with_labels=False,
            node_size=1000, node_color='skyblue')
    nx.draw_networkx_labels(graph, pos)
    for i, (node, (x, y)) in enumerate(pos.items()):
        plt.scatter(x, y, s=1000, c='skyblue', picker=True)
    plt.show()