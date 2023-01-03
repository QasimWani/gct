import ast
from gct.network import Node, Graph
import random
import gct.type_check as type_check
import gct.constants as constants
import graphviz
import os
import shutil
import requests


def generate_random_color():
    """Generate random color in hex format with alpha channel set to 60"""
    return f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}60"


def save_code_to_file(code: str, resource: str):
    if "/" in resource:
        resource = resource.split("/")[-1]
    if not resource.endswith(".py"):
        resource = resource + ".py"
    with open(f"{constants.TEMP_FOLDER}/{resource}", "w") as f:
        f.write(code)


def flush(path: str):
    # if folder doesn't exist, create it and exit. If it does exist, remove all files and create a new temp folder.
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))


def parse_file(resource: str):
    """
    A resource can either be:
    1. URL - in which case we fetch the code and parse it.
    2. Path to a file - in which case we read the file and parse it.
    3. Raw code - in which case we parse it directly.
    """
    if resource.startswith("http"):
        response = requests.get(resource)
        tree = ast.parse(response.text, filename=resource)
        return tree, response.text.splitlines()
    elif resource.endswith(".py"):
        with open(resource, "r") as f:
            tree = ast.parse(f.read(), filename=resource)
            f.seek(0)
            return tree, f.readlines()
    else:
        tree = ast.parse(resource)
        return tree, resource.splitlines()


def get_indent_number(line: str):
    return len(line) - len(line.lstrip())


def get_end_of_function(lines: "list[str]", lineno: int):
    """
    Fetches the end of a function definition by comparing indentation number of the
    first line with the indentation of potential end function.
    @Parameters:
    1. filename: str = file containing function.
    2. lineno: int = line number (0-based indexing) where function of interest starts from.
    @Returns: line number where the function ends.
    """
    start_indent = get_indent_number(lines[lineno])
    for i in range(lineno + 1, len(lines)):
        line = lines[i]
        if (
            get_indent_number(line) <= start_indent
            and line.strip()
            and not line.strip().startswith(")")
        ):
            return i - 1
    return len(lines) - 1


def fetch_full_function(lines: "list[str]", start_lineno: int) -> "list[str]":
    end_lineno = get_end_of_function(lines, start_lineno)
    return lines[start_lineno : end_lineno + 1]


def is_call_node_in_function_of_interest(
    lines: "list[str]", call_node_name: str
) -> bool:
    if not call_node_name:
        # used in node connection logic. In this case, since we only consider
        # function calls, we don't need to check if call_node_name is defined
        # since it's guaranteed that the function node name is unique and only
        # defined once in the output of `fetch_full_function`
        return True

    for line in lines:
        # check if a line is comment
        if line.strip().startswith("#"):
            continue
        if call_node_name in line:
            return True
    return False


def is_line_function_or_class(line: str):
    if line.lstrip().split(" ")[0] == "def" or line.lstrip().split(" ")[0] == "class":
        return True
    return False


def get_immediate_parent(lines: "list[str]", lineno: int, call_node_name: str = None):
    """
    Given a function, fx, find the most immediate parent node.
    In this case, most immediate parent node is the first instance where
    the indentation number is lesser than fx.
    E.g.:
    ```
    def X(): #1
        def Y(): #2
            //code #3
    ```
    In this case, if `Y` is our function of interest, the most immediate
    parent node is function `X` defined at line #1. Core logic is similar
    to `get_end_of_function`, except now we traverse upwards.
    Note that this is not usually the case. Take for example:
    ```
    def X(): #1
        if True:
            def Y(): #2
                //code #3
    ```
    Based on logic above, the most immediate parent node to `Y` should be `if True`,
    but that is not a function or class. Hence, we need to traverse upwards until
    we find a function, class, or we reach the root node. Root node is when indentation
    level is 0.
    To summarize, the two cases to consider:
    1. Root node: indentation level is 0 --> return -1
    2. Function or class node: return line number for that function/class

    @Parameters:
    1. lines: list[str] = relevant lines of code.
    2. lineno:int = line number (0-based indexing) where function of interests starts from.
    3. call_node_name: str = name of function of interest.
    @Returns: line number of immediate parent node.
    """
    assert lineno < len(lines), "lineno out of range"

    if lineno < 0:
        return -1  # root node

    start_indent = get_indent_number(lines[lineno])

    if start_indent == 0:  # at root level
        return -1

    for i in range(lineno, -1, -1):
        line = lines[i]

        ind_num = get_indent_number(line)
        if ind_num >= start_indent or not line.strip():
            continue
        if is_line_function_or_class(line):
            # check if call_node_name is defined in the extracted function
            function_of_interest = fetch_full_function(lines, i)
            if is_call_node_in_function_of_interest(
                function_of_interest, call_node_name
            ):
                return i
        if ind_num == 0 and not line.strip().startswith(")"):  # root node
            return -1

    raise ValueError(f"No parent found. source line: {lineno}")


def find_function_of_interest(name: str, metadata: type_check.Metadata) -> "list[Node]":
    """
    Given a function name, find the function of interest in the node_line_map.
    Ignoring class definition calls for now.

    @Parameters:
    1. node_line_map: dict[int, Node] = maps line number to Node object.
    2. name: str = name of function of interest.
    @Returns: list of potential target `Node` for function of interest.
    """
    prefix, suffix = type_check.get_prefix_and_suffix(name)

    potential_target_nodes: "list[Node]" = []

    if prefix:
        if prefix == constants.SELF_NODE_NAME:
            # get 2nd level parent node
            bilevel_parent_lineno = get_immediate_parent(
                metadata.raw_code, metadata.parent_lineno, name
            )
            # get node name at bilevel parent node line number
            if bilevel_parent_lineno != constants.ROOT_NODE_LINENO:
                bilevel_parent_node = metadata.node_line_map[bilevel_parent_lineno]
                prefix = bilevel_parent_node.name

        potential_target_nodes = type_check.infer_complex_mappings(
            prefix, suffix, metadata
        )
    else:
        potential_target_nodes = type_check.infer_direct_mappings(
            metadata.node_line_map, suffix
        )

    return potential_target_nodes


def add_subgraphs(
    node_representation: Graph,
    graphviz_graph: graphviz.Digraph,
    root: Node,
    visited: set = set(),
):
    """Recursively traverse (depth-first) the graph, `g`, and add corresponding subgraph to `root`."""

    for node in node_representation.G.successors(root):
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
                    bgcolor = generate_random_color()

                c.attr(
                    style="rounded",
                    label=text,
                    color="black",
                    cluster="true",
                    bgcolor=bgcolor,
                )
                add_subgraphs(node_representation, c, node, visited)
        else:
            text = node.__repr__()
            style = "rounded"
            bgcolor = "transparent"
            shape = ""

            if node.type == "class":
                text = f"< <B>{node.__repr__()}</B> >"
                style = "rounded, filled"
                shape = "box"
                bgcolor = generate_random_color()

            graphviz_graph.node(
                node.id,
                text,
                style=style,
                shape=shape,
                fillcolor=bgcolor,
            )

            add_subgraphs(node_representation, graphviz_graph, node, visited)
