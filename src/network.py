import networkx as nx
import matplotlib.pyplot as plt

# Contains definitions for node, edge, NodeCreation, and EdgeCreation graph representations


class Node:
    def __init__(
        self,
        line_start: int,
        line_end: int,
        name: str,
        type: str = None,
    ):
        self.line_start = line_start
        self.line_end = line_end
        self.name = name
        self.type = type  # options: [function, class]

    def __repr__(self) -> str:
        return f"{self.name}({self.line_start}, {self.line_end}, {self.type})"


class Graph:
    def __init__(self):
        self.G = nx.DiGraph()

    def add_edge(self, node1: Node, node2: Node):
        self.G.add_edge(node1, node2)

    def draw_graph(self):
        nx.draw_networkx(self.G)
        plt.show()
