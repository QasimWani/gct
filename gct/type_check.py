import ast
from gct.network import Node, Graph
from gct.constants import NODE_NAMES_TO_IGNORE
from collections import namedtuple


class Metadata(
    namedtuple(
        "Metadata", ["tree", "raw_code", "node_graph", "node_line_map", "parent_lineno"]
    )
):
    tree: ast
    raw_code: "list[str]"
    node_graph: Graph
    node_line_map: "dict[int, Node]"
    parent_lineno: int  # Line number where function of interest is defined


def helper_search_definition(tree, variable_name):
    """
    Recursive function to search for the definition of a variable in an AST.
    Note: This only searches the latest definition of a variable since Python is dynamically typed.
    So the results may not be accurate if the variable is redefined.

    E.g.:
    ```
    class A:
        def func(self):
            pass
    var = A()
    x = var.func()
    ```
    In this case, we want to find the definition of `var` in the AST.
    Using the AST, we can find the definition of `var` in the `Assign` node.
    We can also have multiple targets in the assignment. E.g:
    ```
    class A:
        def func(self):
            pass
    temp, var = None, A()
    x = var.func()
    ```
    In this case, var is defined in the `Assign` node with two targets. This is stored as an ast.Tuple node.
    So we must traverse through all the elements in the tuple to find the definition corresponding to `var`.
    """

    # Iterate through the nodes in the AST
    for node in ast.iter_child_nodes(tree):
        # Both cases work only if the node is of type `Assign`
        if isinstance(node, ast.Assign):

            for target in node.targets:
                # case I: target is a single variable
                if isinstance(target, ast.Name) and target.id == variable_name:
                    return node

                # case II: target is a tuple
                if isinstance(target, ast.Tuple):
                    for el in target.elts:
                        if isinstance(el, ast.Name) and el.id == variable_name:
                            return node

        # Recursively search for the definition in child nodes
        definition = helper_search_definition(node, variable_name)
        if definition:
            return definition
    return None


def search_for_definition(tree: ast, name: str) -> list:
    """
    Find where a variable has been defined.
    @Parameters:
    1. tree: ast = AST of the file.
    2. name: str = name of variable to search for.
    @Returns: list of potential targets for the variable. If empty, no target has been found.
    """
    if name in NODE_NAMES_TO_IGNORE:
        return []

    result = helper_search_definition(tree, name)
    potential_target_nodes = []

    if not result:
        return potential_target_nodes
    try:
        if isinstance(result.value, ast.Call):
            if isinstance(result.value.func, ast.Attribute):
                potential_target_nodes.append(result.value.func.attr)
            else:
                if isinstance(result.value.func, ast.Name):
                    potential_target_nodes.append(result.value.func.id)
                elif isinstance(
                    result.value.func, ast.Subscript
                ):  # BUG: this is a hacky fix for the case where the function is a subscript
                    potential_target_nodes.append(result.value.func.value.id)
        elif isinstance(result.value, ast.Tuple):
            for node in result.value.elts:
                if isinstance(node, ast.Call):
                    potential_target_nodes.append(node.func.id)
                elif isinstance(node, ast.Name):
                    potential_target_nodes.append(node.id)
    except Exception as e:
        print(f"Error: {e}")

    return potential_target_nodes


def get_prefix_and_suffix(name: str) -> "tuple[str, str]":
    """
    Given a function name, return the prefix and suffix.
    E.g.:
    ```
    1. Class.func --> prefix is `Class` and suffix is `func`
    2. func --> prefix is None and suffix is `func`
    3. module.Class.func --> prefix is `module.Class` and suffix is `func`
    ```
    Note: we ignore (3) for now since GCT currently only handles file-level tracing. This means that we're also
    not including subclasses that belong to the same file. It's pretty uncommon to have multiple subclasses in the same file.
    So to keep things simple for now and optimize for the common case, it's fine to ignore this. But in the future,
    this should be handled.

    @Parameters:
    1. name: str = name of function of interest.
    @Returns: tuple of prefix and suffix.
    """
    prefix = None
    suffix = name

    if "." in name:
        splits = name.split(".")
        if len(splits) == 2:
            prefix, suffix = splits
        else:
            suffix = splits[-1]
    return prefix, suffix


def infer_complex_mappings(prefix: str, suffix: str, metadata: Metadata):
    """
    Infer mappings for complex cases.
    E.g.:
    ```
    1. Class.func
    2. c.func(), where c = Class
    ```
    Case I is trivial. We just need to find the node with prefix. And get all chldren from that node that has suffix.
    Case II is a bit more tricky. We need to find the code definition of c, and then find the node with correct prefix.
    From there, we can get all children with suffix.
    @Parameters:
    1. prefix: str = prefix of function name.
    2. suffix: str = suffix of function name.
    3. metadata: Metadata = metadata for the file.
    """
    tree: ast = metadata.tree
    node_graph: Graph = metadata.node_graph
    node_line_map: "dict[int, Node]" = metadata.node_line_map
    potential_target_nodes: "list[Node]" = []

    # Case I: prefix is a class/method name
    prefix_target_nodes = find_nodes_by_name(prefix, node_line_map.values())
    # get children nodes for each prefix node
    for node in prefix_target_nodes:
        children_nodes = node_graph.get_children_nodes(node)
        suffix_target_nodes = find_nodes_by_name(suffix, children_nodes)
        potential_target_nodes.extend(suffix_target_nodes)

    # Case II: prefix is a variable
    if not potential_target_nodes:
        potential_names = search_for_definition(tree, prefix)

        for potential_name in potential_names:
            prefix_target_nodes = find_nodes_by_name(
                potential_name, node_line_map.values()
            )
            for node in prefix_target_nodes:
                children_nodes = node_graph.get_children_nodes(node)
                suffix_target_nodes = find_nodes_by_name(suffix, children_nodes)
                potential_target_nodes.extend(suffix_target_nodes)

    return potential_target_nodes


def find_nodes_by_name(target_node_name: str, nodes: "list[Node]") -> "list[Node]":
    """
    Find all nodes with the given name.
    @Parameters:
    1. target_node_name: str = name of node to search for.
    2. nodes: list[Node] = list of nodes to search through.
    @Returns: list of nodes with the given `target_node_name`.
    """
    potential_target_nodes: "list[Node]" = []
    for node in nodes:
        if node.name == target_node_name:
            potential_target_nodes.append(node)
    return potential_target_nodes


def infer_direct_mappings(node_line_map: "dict[int, Node]", name: str) -> "list[Node]":
    """
    Handles the case where the function of interest is a direct mapping to a node.
    E.g.:
    ```
    def func():
        pass
    func()
    ```
    In this case, `func` is a direct mapping to the `Node` object corresponding to the function definition.

    @Parameters:
    1. node_line_map: dict[int, Node] = maps line number to Node object.
    2. suffix: str = suffix of function of interest.
    @Returns: list of potential targets for the function of interest.
    """
    return find_nodes_by_name(name, node_line_map.values())
