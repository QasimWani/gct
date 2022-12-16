import graphviz
import utils
from parse import extract

# filename = "examples/arithmetics.py"
filename = "examples/complex_structure.py"
tree, raw_code = utils.parse_file(filename)

node_representation, edge_representation = extract(tree, raw_code)


node_representation.group_nodes_by_level()
# generate heirarchical clustering.
clusters = node_representation.level_clustering
node_representation.print_graph_by_levels()

# TODO: Convert `clusters` information to a graph using graphviz

# all subgraphs should be vertical

# g = graphviz.Digraph("G", filename="cluster_edge.gv", engine="neato")
# g.attr(compound="true", rankdir="LR")

# for i, (parent, children) in enumerate(clusters.items()):
#     # create subgraphs and display them vertically
#     with g.subgraph(name=f"cluster_{i}") as c:
#         random_color = utils.generate_random_color()
#         c.attr(style="rounded, filled", color=random_color, label=parent.__repr__())
#         c.node_attr.update(
#             style="rounded, filled",
#             shape="box",
#             color="white",
#             fontsize="10",
#             rank="same",
#         )
#         # add all nodes horizontally in the subgraph
#         for child in children:
#             if child.type == "class":
#                 continue
#             c.node(child.__repr__())


# g.view()
