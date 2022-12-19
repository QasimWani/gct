import graphviz
import utils
from parse import extract
import networkx as nx
from network import Node

filename = "examples/arithmetics.py"
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
            with graphviz_graph.subgraph(name=f"cluster_{node.__repr__()}") as c:
                c.attr(style="rounded", label=node.__repr__())
                add_subgraphs(c, node, g, visited)
        else:
            graphviz_graph.node(node.__repr__())
            add_subgraphs(graphviz_graph, node, g, visited)


g = graphviz.Digraph("G", filename="clusters.gv", engine="dot")
g.attr(compound="true", rankdir="TB")

root = list(node_representation.G.nodes)[0]
add_subgraphs(g, root, node_representation.G)

# create edges
edges = list(edge_representation.G.edges)
for u, v in edges:
    g.edge(u.__repr__(), v.__repr__())

g.view()
