import networkx as nx
import matplotlib.pyplot as plt

# Contains definitions for node, edge, NodeCreation, and EdgeCreation graph representations

class Node:
    def __init__(self, line_start:int, line_end:int, name:str, children=[], parent=None, edges=[]):
        self.line_start = line_start
        self.line_end = line_end
        self.name = name

        self.children:list[Node] = children
        self.parent:Node = parent
        self.edges:list[Node] = edges

    def is_child_node(self, node):
        """ Return true if `node` is a child node of `self` """
        for child in self.children:
            if child == node:
                return True
        return False
    def is_parent_node(self, node):
        """ Return true if `node` is parent node of `self` """
        return node == self.parent

    def __repr__(self) -> str:
        return f"{self.name}({self.line_start}, {self.line_end})"

class NodeRepresentationGraph:
    def __init__(self):
        self.G = nx.DiGraph()

    def add_edge(self, node1:Node, node2:Node):
        self.G.add_edge(node1, node2)

    def draw_graph(self):
        nx.draw_networkx(self.G)
        plt.show()