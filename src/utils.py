import ast
from network import Node
import random


def generate_random_color():
    """Generate random primary color gradient"""
    return f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"


def parse_file(filename):
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
    is_line_function_or_class = lambda line: line.strip().startswith(("def", "class"))

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


def find_function_of_interest(node_line_map: dict[int, Node], name: str) -> list[Node]:
    """
    Given a function name, find the function of interest in the node_line_map.
    Ignoring class definition calls for now.

    @Parameters:
    1. node_line_map: dict[int, Node] = maps line number to Node object.
    2. name: str = name of function of interest.
    @Returns: list of potential target `Node` for function of interest.
    """
    potential_target_nodes: list[Node] = []
    for node in node_line_map.values():
        if node.name == name and node.type == "function":
            potential_target_nodes.append(node)
    return potential_target_nodes
