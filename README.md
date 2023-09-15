# Pampered pets attack tree application

Word count: 1187

This application is an attack tree visualizer, which allows users to visualize a JSON file that represents an attack tree, and allows the user to update attack tree values

# Report
Dear Cathy,

As requested, a python application was created that can accept an attack tree specification in the industry standard format known as JSON (Tentilucci et al. 2015). The attack trees were created with research potential attack vectors from a variety of sources, please see the individual example JSON files provided for detailed sources of potential vectors as well as their respective estimated costs. Three potential scenarios cases were considered based on the risk identification report (Mian, 2023): 

## Local supplier issues
![image](https://github.com/haarismian/attack_tree_project/assets/13083798/503b5d9e-52d2-4e5c-a406-9e6d49f7aa25)

## Challenges in the digitization process
![image](https://github.com/haarismian/attack_tree_project/assets/13083798/c96f3733-c512-46d2-8b6e-9349c3401cd1)

## A potential data breach after the digitization process is complete
![image](https://github.com/haarismian/attack_tree_project/assets/13083798/893608af-5b81-4741-8000-fdf5a6a1e9dc)




# Code functionalities

## Import and utility setup

- **json**: Used to work with JSON data.
- **matplotlib.pyplot**: Utilized for data visualization using various plot types.
- **networkx**: To create, manipulate, and study the complex networks of nodes and edges in the hierarchical tree structure.
- **graphviz_layout**: Facilitates better layout and visualization of the graph using Graphviz.

## Recursive Functionality

- **add_edges**: A recursive function to add edges and nodes to the graph parsed from the JSON data. It is capable of handling nested hierarchical data by iterating through child nodes recursively.

## Node and Edge Management

- **find_parent_values**: Finds and sums the values of all ancestor nodes of a specific node in the graph.
- **visualize_attack_tree**: Visualizes the hierarchical tree structure using NetworkX and Matplotlib. It incorporates the `add_edges` function to build the graph and uses Graphviz for layout.

## Interactive Graph Visualization

- **on_pick**: Event handler for node clicks during visualization, allowing users to update node values interactively.
- **update_labels**: Updates the labels of the nodes in the graph, to reflect any changes in node values.
- **draw_initial_graph**: Initiates the drawing of the graph using Matplotlib.
- **draw_graph**: Draws the graph with given node positions and labels, allowing for re-drawing when updates are made.
- **redraw_graph**: Clears the existing graph visualization and redraws it with updated labels to showcase changes in real-time.

## Graph Drawing

- **draw_initial_graph**: Sets the initial state for the graphical visualization, invoking the draw_graph function for the initial graph representation.
- **draw_graph**: Facilitates the actual drawing of the graph based on the current state of node positions and labels.

## Path Summation and Reporting

- **sum_routes**: Sums individual paths recursively and displays each path with its corresponding sum to the user, giving detailed insights into various paths and their cumulative values in the hierarchical tree structure.

## Main Script Execution

- **if __name__ == "__main__"**: Specifies the JSON file path and executes the `sum_routes` and `visualize_attack_tree` functions to visualize the hierarchical tree structure and display the summed values of individual paths to the console.


# Installation
1. Ensure you have the `Python` programming language installed - if you have python 3 installed you will be using the `python3` command, if you do not, then you will use the `python` command
2. Ensure you have the `pip` package manager installed by following the instructions on this page `https://pip.pypa.io/en/stable/installation/`
3. Using the terminal navigate to the folder of the code submission with the file `requirements.txt`. This will be in the root directory
4. Use the command `pip install -r requirements` to install all project dependencies. These dependencies are necessary for the project to run and include things like matplotlib or networkx. Please see the requirements.txt file for the full details.
5. Once all dependencies are installed, use the command `python app.py` or `python3 app.py` to run the application.

# Test cases:

Python’s unittest module and assert statements were used to test functionalities below:

1. Successfully adding correct edges
2. Successfully summing values of all the node paths
3. Successfully adding all the parent values of nodes

# SDLC reflections:

## Changes from design docs

Changes were made to the original design to improve code robustness. For example, a state management system was implemented that transitions from accelerating, braking, and stationary. Unnecessary car properties such as braking pressure and steering wheel angle were removed, and more feasible properties such as acceleration decrement and compass direction were added. Finally, several classes and Enums were added to accommodate real-life uses that were not in the original design.

## Strengths

The app visualizes and manipulates hierarchical tree data derived from a JSON file. It utilizes the powerful NetworkX library to create and manipulate complex networks of nodes and edges, along with matplotlib to visualize these networks. The script is particularly distinguished by its interactive functionalities: users can click on individual nodes in the visualized tree to update node values, with a prompt guiding them to input a new value while also displaying the summed values of the node’s ancestors to inform their decision. This script also harbors a rich variety of functionalities beyond visualization: it can sum the values along different routes in the tree, returning a comprehensive detail of each path and its respective sum, effectively illustrating the cumulative impacts or risks at different endpoints in the hierarchical structure. This is complemented by a recursive function to add nodes and edges to the network, a technique that optimizes for both readability and performance, keeping the script DRY (Don't Repeat Yourself) and facilitating potential extensions or modifications to the tree structure handling. Moreover, the implementation adheres to best practices such as well-structured function documentation and appropriate error handling to guide the user effectively during interactive input sessions. The decision to separate drawing functions and update labels maintains code modularity, making it easier to manage and update the script in the future. This foresight in design makes the script not only functional but also user-friendly and maintainable, catering to a wide range of potential users from data analysts to cybersecurity experts analyzing attack trees.

## Challenges

During the development phase, one of the primary obstacles encountered was navigating the constraints imposed by the limitations of third-party libraries, a common occurrence in sophisticated software engineering environments. The crux of the issue centered on leveraging the Matplotlib library optimally, a pivotal tool enlisted for rendering the attack tree structures.

Due to Matplotlib's ostensibly inadequate built-in support for discerning the exact node activated during the `on_pick` event — a critical feature for enhancing interactivity in the graphical representation. I devised a strategy that encompasses intercepting the event emitter object to glean critical information, a process facilitated by a systematic traversal of the original JSON data to pinpoint the exact node correspondent to the action instigated, successfully augmenting the library's native capabilities.

## Future Room for Improvement:

1.  In subsequent versions of the application, it would be prudent to integrate functionalities facilitating easier data import and export, thus enhancing interoperability with other tools and systems. In parallel, the user interface could be refined to offer more intuitive navigation and a richer visual representation of the attack trees, possibly through the introduction of custom node icons and color-coded risk levels.
2.  Greater interactivity which includes the ability to click and drag to move nodes around
