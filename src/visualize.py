import graphviz
import utils
from parse import extract
import networkx as nx
from network import Node
import argparse

# use argparse to parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "--filename",
    type=str,
    default="examples/arithmetics.py",
    help="Path to the file/URL to visualize",
)
filename = parser.parse_args().filename

# filename = "examples/arithmetics.py"
# filename = "https://raw.githubusercontent.com/timesler/facenet-pytorch/555aa4bec20ca3e7c2ead14e7e39d5bbce203e4b/models/mtcnn.py"
# filename = "examples/complex_structure.py"

tree, raw_code = utils.parse_file(filename)

node_representation, edge_representation = extract(tree, raw_code)


node_representation.group_nodes_by_level()
# generate heirarchical clustering.


def add_subgraphs(
    graphviz_graph: graphviz.Digraph, root: Node, g: nx.DiGraph, visited: set = set()
):
    """Recursively traverse (depth-first) the graph, `g`, and add corresponding subgraph to `root`."""
    for node in g.successors(root):
        node: Node = node
        if node in visited:
            continue
        visited.add(node)
        if not node_representation.is_leaf_node(node):  # create subgraph
            with graphviz_graph.subgraph(name=f"{node.id}") as c:
                c.node(node.id, style="invis", fontsize="0")

                bgcolor = "transparent"
                text = node.__repr__()
                if node.type == "class":
                    text = f"< <B>{text}</B> >"
                    bgcolor = utils.generate_random_color()

                c.attr(
                    style="rounded",
                    label=text,
                    color="black",
                    cluster="true",
                    bgcolor=bgcolor,
                )
                add_subgraphs(c, node, g, visited)
        else:
            graphviz_graph.node(node.id, label=node.__repr__())
            add_subgraphs(graphviz_graph, node, g, visited)


g = graphviz.Digraph("G", engine="dot")
g.attr(compound="true", rankdir="TB")

try:
    root = list(node_representation.G.nodes)[0]
    add_subgraphs(g, root, node_representation.G)

    # create edges
    edges = list(edge_representation.G.edges)
    for u, v in edges:
        g.edge(u.id, v.id)

    g.view()

except:
    print("LOL.")
