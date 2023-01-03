import networkx as nx
import uuid


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
        self.id = uuid.uuid1().hex

    def __repr__(self) -> str:
        return f"{self.name} #{self.line_start + 1}"


class Graph:
    def __init__(self):
        self.G = nx.DiGraph()
        self._level_clustering = {}

    @property
    def level_clustering(self):
        return self._level_clustering

    def add_edge(self, node1: Node, node2: Node):
        self.G.add_edge(node1, node2)

    def get_all_nodes(self) -> "list[Node]":
        return list(self.G.nodes)

    def get_root_node(self) -> Node:
        if not self.get_all_nodes():
            return None
        return self.get_all_nodes()[0]

    def get_parent_node(self, node: Node) -> Node:
        """
        > Given a node, return the parent node

        :param node: The node to get the parent of
        :type node: Node
        :return: The parent node of the node passed in.
        """
        try:
            return list(self.G.predecessors(node))[0]
        except:
            return None  # root node

    def get_children_nodes(self, node: Node) -> "list[Node]":
        return list(self.G.successors(node))

    def group_nodes_by_level(self):
        if self._level_clustering:
            return

        for node in self.get_all_nodes():
            parent_node = self.get_parent_node(node)
            if parent_node is None:
                continue
            self._level_clustering[parent_node] = self.get_children_nodes(parent_node)

    def is_leaf_node(self, node: Node) -> bool:
        return len(self.get_children_nodes(node)) == 0

    def print_graph_by_levels(self):
        """
        Print the graph by levels.
        Example:
        ```
        class A:
            def b():
                def c():
                    def d():
                        pass
            class B:
                def test():
                    pass
        ```
        Running `print_graph_by_levels()` will print:
        ```
        --- A(1, 8, class) ---
            b(2, 5, function)
            c(3, 5, function)
            d(4, 5, function)
            B(6, 8, class)
        --- B(6, 8, class) ---
            test(7, 8, function)
        ```
        Note how the nodes are printed by breath-first search order & not depth-first.
        Ideally, the output should look something like this:
        ```
        --- A(1, 8, class) ---
            b(2, 5, function)
            c(3, 5, function)
            d(4, 5, function)
            --- B(6, 8, class) ---
                test(7, 8, function)
        ```
        But you can leverage information stored in `self._level_clustering` to do this.
        """
        self.group_nodes_by_level()

        for parent_node, children_nodes in self._level_clustering.items():
            parent_node: Node = parent_node
            children_nodes: "list[Node]" = children_nodes

            print(f"--- {parent_node} ---")
            for child_node in children_nodes:
                print(f"\t{child_node}")
