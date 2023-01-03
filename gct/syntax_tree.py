import ast
from gct.network import Node
from collections import deque


class FunctionCallVisitor(ast.NodeVisitor):
    """Extract all function calls"""

    def __init__(self):
        self._name = deque()

    @property
    def name(self):
        # return self._name[-1]
        return ".".join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name.appendleft(node.id)

    def visit_Attribute(self, node):
        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
        except AttributeError:
            self.generic_visit(node)


class UserDefinedFuncVisitor(ast.NodeVisitor):
    """Extract all user defined functions and classes"""

    def __init__(self):
        self.node: Node = None

    def create_node(self, node: ast.AST, node_name: str, type: str):
        end_lineno = node.lineno - 1 if "end_lineno" in dir(node) else str(None)
        self.node = Node(node.lineno - 1, end_lineno, node_name, type)

    def visit_Lambda(self, node: ast.Lambda):
        raise NotImplementedError("Lambda functions are not supported yet")
        self.create_node(node, "lambda", "function")

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.create_node(node, node.name, "function")

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.create_node(node, node.name, "function")

    def visit_ClassDef(self, node: ast.ClassDef):
        self.create_node(node, node.name, "class")
