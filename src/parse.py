import ast
import utils
from syntax_tree import FunctionCallVisitor, UserDefinedFuncVisitor
from network import Node, NodeRepresentationGraph

def extract(tree:ast, raw_code:list[str]):
    """ 2 pass algorithm """
    node_line_map:dict[Node] = {-1: Node(-1, len(raw_code), "root")}
    
    # Node creation
    for node in ast.walk(tree):        
        if isinstance(node, ast.Call):
            call_visitor = FunctionCallVisitor()
            call_visitor.visit(node.func)
            
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            func_visitor = UserDefinedFuncVisitor()
            func_visitor.visit(node)
            node_line_map[func_visitor.node.line_start] = func_visitor.node

    # Node connection
    g = NodeRepresentationGraph()
    
    for start_lineno, node in node_line_map.items():
        node:Node = node
        if start_lineno == -1: # root node has no parent. skip connection
            continue 
        
        parent_lineno:int = utils.get_immediate_parent(raw_code, start_lineno)
        parent_node:Node = node_line_map[parent_lineno]

        g.add_edge(parent_node, node)

filename = "test/complex_structure.py"
tree, raw_code = utils.parse_file(filename)

extract(tree, raw_code)