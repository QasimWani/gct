""" 
Graphical Code Tracer (GCT) is a static code analysis tool that generates 
a graphical representation of a Python program. It shows how different parts
of the program interact with each other. GCT is built on top of the AST module
and thus isn't always 100% accurate due to the dynamic nature of Python.

GCT, however, still provides a good overview of the program and can be used
to quickly identify potential bugs, understand the general flow of a program,
and onboard new developers to any python codebase.

GCT is currently limited to file-level tracing. This means that it can only
trace functions and classes that are defined in the same file. If you enjoy
GCT, please consider contributing to the project to extend its functionality.
https://github.com/QasimWani/gct


Running GCT on any python3 file is as simple as:

>>> import gct.api as api
>>> path = "example/arithmetics.py"
>>> graph, code = api.run(path)
>>> api.render(graph, file_name="temp/graph", output_format="pdf")

If you want to load the svg object in memory instead of saving it to a file, 
leave `file_name` in api.run as None.
>>> svg_as_string = api.run(graph)

"""
import graphviz

import gct.utils as utils
from gct.parse import extract
import time
from gct.constants import TEMP_FOLDER, GRAPH_FOLDER_DEFAULT_NAME


def run(resource_name: str) -> "list[graphviz.Digraph, str]":
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

        print(f"Successfully generated graph in {time.time() - start_time:.2f} seconds")
        return g, "\n".join(raw_code)

    raise Exception("No user-defined functions/class definitions found.")


def render(
    graph: graphviz.Digraph, file_path: str = None, output_format: str = "svg"
) -> str:
    """
    Renders the graphviz object to a file.
    @Parameters:
    1. graphviz_object: graphviz.Digraph = Graphviz object to render.
    2. file_path: str = file path to save the output to. If None, the svg output (str) will be returned.
    3. output_format: str = Output format. Defaults to svg. Other formats include "png", "pdf".
    """
    updated_file_path = (
        f"{TEMP_FOLDER}/{GRAPH_FOLDER_DEFAULT_NAME}"
        if file_path is None
        else file_path
    )

    graph.render(updated_file_path, format=output_format, view=file_path is not None)

    if file_path is None:
        # Read the svg file and return it as a string
        with open(f"{updated_file_path}.{output_format}", "r") as f:
            result = f.read()
            utils.flush(f"{TEMP_FOLDER}/")
            return result

    return ""
