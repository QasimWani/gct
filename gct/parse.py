import ast
import gct.utils as utils
from gct.syntax_tree import FunctionCallVisitor, UserDefinedFuncVisitor
from gct.network import Node, Graph
import gct.constants as constants
from gct.type_check import Metadata


def extract(tree: ast, raw_code: "list[str]"):
    """2 pass algorithm"""

    node_line_map: "dict[int, Node]" = {
        constants.ROOT_NODE: Node(constants.ROOT_NODE_LINENO, len(raw_code), "root")
    }
    node_creation_graph = Graph()
    edge_creation_graph = Graph()

    # Node creation
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            func_visitor = UserDefinedFuncVisitor()
            func_visitor.visit(node)
            node_line_map[func_visitor.node.line_start] = func_visitor.node

    # Node connection
    for start_lineno, node in node_line_map.items():
        node: Node = node
        if (
            start_lineno == constants.ROOT_NODE_LINENO
        ):  # root node has no parent. skip connection
            continue
        parent_lineno: int = utils.get_immediate_parent(raw_code, start_lineno)
        parent_node: Node = node_line_map[parent_lineno]

        node_creation_graph.add_edge(parent_node, node)
    # Edge connection
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            call_visitor = FunctionCallVisitor()
            call_visitor.visit(node.func)

            # 1. find immediate parent (i.e. scope of where this function was called)
            # 2. find what function is being called (i.e. scope of where this function was defined)
            # 3. connect (1) to (2) via `Edge`

            line_start_source_function = utils.get_immediate_parent(
                raw_code, node.lineno - 1, call_visitor.name
            )

            source_node: Node = None

            if line_start_source_function in node_line_map:
                source_node = node_line_map[line_start_source_function]
            else:
                continue  # skip if source function is not defined in the file

            potential_target_nodes = utils.find_function_of_interest(
                call_visitor.name,
                Metadata(
                    tree,
                    raw_code,
                    node_creation_graph,
                    node_line_map,
                    line_start_source_function,
                ),
            )

            # ignore all root connections for now
            if source_node.line_start == constants.ROOT_NODE_LINENO:
                continue

            # create an edge for each potential target node with source node
            for target_node in potential_target_nodes:
                edge_creation_graph.add_edge(source_node, target_node)

    return node_creation_graph, edge_creation_graph
