class Node:
    def __init__(self, line_start:int, line_end:int, name:str, children=[], parent=None, edges=[]):
        self.line_start = line_start
        self.line_end = line_end
        self.name = name

        self.children:list[Node] = children
        self.parent:Node = parent
        self.edges:list[Node] = edges

    def add_parent(self, node):
        """ Node creation """
        self.parent = node
    def add_child(self, node):
        """ Node creation """
        self.children.append(node)
        
    def add_edge(self, node):
        """ Edge creation """
        self.edges.append(node)