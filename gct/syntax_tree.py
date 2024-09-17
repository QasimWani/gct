import ast
from gct.network import Node
from collections import deque
from gct.summarize import CodeSummarizer
from gct.utils import fetch_full_function

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

    def __init__(self, raw_code: "list[str]", summarize: bool):
        self.node: Node = None
        self.summarize = summarize
        self.raw_code = raw_code
        if self.summarize:
            self.code_summarizer = CodeSummarizer()

    def create_node(self, node: ast.AST, node_name: str, type: str):
        end_lineno = node.lineno - 1 if "end_lineno" in dir(node) else str(None) # FIXME: @qasim is this correct?
        lines = fetch_full_function(self.raw_code, node.lineno - 1)
        summary = self.code_summarizer.summarize(lines) if self.summarize else None
        self.node = Node(node.lineno - 1, end_lineno, node_name, type, summary)

    def visit_Lambda(self, node: ast.Lambda):
        raise NotImplementedError("Lambda functions are not supported yet")
        self.create_node(node, "lambda", "function")

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.create_node(node, node.name, "function")

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.create_node(node, node.name, "function")

    def visit_ClassDef(self, node: ast.ClassDef):
        self.create_node(node, node.name, "class")
