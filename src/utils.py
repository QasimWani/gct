import ast
from network import Node, Graph
import random
import type_check as tc
import constants


def generate_random_color():
    """Generate random color in hex format with alpha channel set to 60"""
    return f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}60"


def parse_file(filename: str):
    if filename.startswith("http"):
        import requests

        response = requests.get(filename)
        tree = ast.parse(response.text, filename=filename)
        return tree, response.text.splitlines()

    with open(filename, "r") as f:
        tree = ast.parse(f.read(), filename=filename)
        f.seek(0)
        return tree, f.readlines()


def get_indent_number(line: str):
    return len(line) - len(line.lstrip())


def get_immediate_parent(lines: list[str], lineno: int):
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
    to `fetch_end_of_function`, except now we traverse upwards.
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
    @Returns: line number of immediate parent node.
    """
    assert lineno < len(lines), "lineno out of range"

    if lineno < 0:
        return -1  # root node

    start_indent = get_indent_number(lines[lineno])

    def is_line_function_or_class(line: str):
        if line.strip().split(" ")[0] == "def" or line.strip().split(" ")[0] == "class":
            return True
        return False

    if start_indent == 0:  # at root level
        return -1
    for i in range(lineno, -1, -1):
        line = lines[i]

        ind_num = get_indent_number(line)

        if ind_num >= start_indent or not line.strip():
            continue
        if is_line_function_or_class(line):
            return i
        if ind_num == 0:
            return -1

    raise ValueError(f"No parent found. source line: {lineno}")


def find_function_of_interest(name: str, metadata: tc.Metadata) -> list[Node]:
    """
    Given a function name, find the function of interest in the node_line_map.
    Ignoring class definition calls for now.

    @Parameters:
    1. node_line_map: dict[int, Node] = maps line number to Node object.
    2. name: str = name of function of interest.
    @Returns: list of potential target `Node` for function of interest.
    """
    prefix, suffix = tc.get_prefix_and_suffix(name)

    potential_target_nodes: list[Node] = []

    if prefix:
        if prefix == constants.SELF_NODE_NAME:
            # get 2nd level parent node
            bilevel_parent_lineno = get_immediate_parent(
                metadata.raw_code, metadata.parent_lineno
            )
            # get node name at bilevel parent node line number
            if bilevel_parent_lineno != constants.ROOT_NODE_LINENO:
                bilevel_parent_node = metadata.node_line_map[bilevel_parent_lineno]
                prefix = bilevel_parent_node.name

        potential_target_nodes = tc.infer_complex_mappings(prefix, suffix, metadata)
    else:
        potential_target_nodes = tc.infer_direct_mappings(
            metadata.node_line_map, suffix
        )

    return potential_target_nodes
