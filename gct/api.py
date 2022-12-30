import graphviz

import gct.utils as utils
from gct.parse import extract
import time
from gct.constants import TEMP_FOLDER


def run(resource_name: str) -> list[graphviz.Digraph, str]:
    """
    Runs GCT on a given resource and returns the graphviz object.
    @Parameter:
    1. resource_name: str = Path to the file/URL to generate graph for.
    @Returns:
    1. graphviz.Digraph object. To render the graph, call the render() method on the object.
    2. str: The raw code corresponding to `resource_name`.
    """
    # Flush temp folder. If it doesn't exist, create it.
    utils.flush(f"{TEMP_FOLDER}/")

    start_time = time.time()

    # Get the AST and raw code
    tree, raw_code = utils.parse_file(resource_name)
    # Extract relevant components -- node connection and edge mapping
    node_representation, edge_representation = extract(tree, raw_code)
    # Heirarchical clustering
    node_representation.group_nodes_by_level()
    # Define graphviz graph
    g = graphviz.Digraph("G", filename=f"{TEMP_FOLDER}/graph", engine="dot")
    g.attr(compound="true", rankdir="LR", ranksep="1.0")

    # Create visual graph representation
    root = node_representation.get_root_node()
    if root:
        utils.add_subgraphs(node_representation, g, root)

        # create edges
        edges = list(edge_representation.G.edges)
        for u, v in edges:
            g.edge(u.id, v.id)

        # g.render(filename=f"{TEMP_FOLDER}/graph", format="svg")

        print(f"Successfully generated graph in {time.time() - start_time:.2f} seconds")
        return g, "\n".join(raw_code)

    raise Exception("No user-defined functions/class definitions found.")
