import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas

from Online_MINADM_algorithm import online_min_adm_algorithm


class Handle_graphs:
    def __init__(self, layout, ring_or_path):
        self.ax = None
        self.canvas = None
        self.layout = layout
        self.ring_or_path = ring_or_path
        self.number_of_nodes = 0
        self.algorithm = online_min_adm_algorithm()

    def display_graph(self, number_of_nodes):
        self.number_of_nodes = number_of_nodes
        self.algorithm.__init__()
        fig = plt.figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        ax.axis('off')
        self.ax = ax
        self.canvas = canvas
        if self.ring_or_path == "path":
            self.algorithm.create_path_graph(number_of_nodes)
            self.display_path_graph()
        else:
            self.algorithm.create_cycle_graph(number_of_nodes)
            self.display_ring_graph()

    def display_path_graph(self):
        graph = self.algorithm.graph
        pos = {node: (node, 0) for node in graph.nodes}
        nx.draw_networkx(graph, ax=self.ax, pos=pos, node_size=500)
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.path_graph_layout.addWidget(self.canvas)

    def display_ring_graph(self):
        graph = self.algorithm.graph
        pos = nx.circular_layout(graph, scale=2.0)
        # nx.draw_networkx(self.ring_topology_algorithm.graph, ax=ax, with_labels=True, node_size=1000, pos=pos)
        nx.draw_networkx_nodes(graph, pos=pos, ax=self.ax, node_size=500)
        edge_list = list()
        ax = self.ax
        number_of_nodes = self.number_of_nodes
        for i in range(self.number_of_nodes - 1):
            edge_list.append((i + 1, i + 2))
        nx.draw_networkx_edges(graph, edgelist=edge_list, pos=pos
                               , ax=ax, connectionstyle='arc3,rad=0.2'
                               , arrows=True)

        nx.draw_networkx_edges(graph, edgelist=[(number_of_nodes, 1)], pos=pos
                               , ax=ax, connectionstyle='arc3,rad=0.2'
                               , arrows=True)
        nx.draw_networkx_labels(graph, pos, ax=ax)
        ax.set_aspect('equal')
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.layout.addWidget(self.canvas)

    def add_light_path(self, path):
        self.algorithm.add_light_path(path)
        starting_node = self.algorithm.paths[-1][0]
        ending_node = self.algorithm.paths[-1][-1]
        color = self.algorithm.path_colour[-1]
        for i in range(len(self.algorithm.colours)):
            if self.algorithm.colours[i] == color:
                index = i
                break
        if self.ring_or_path == "path":
            self.ax.plot([starting_node, ending_node - 0.1], [index + 1, index + 1], color=color)
        else:
            pos = nx.circular_layout(self.ring_topology_algorithm.graph, scale=2.5 + 0.5 * index)
            edge_list = list()
            for i in range(len(path) - 1):
                edge_list.append((path[i], path[i + 1]))
            nx.draw_networkx_edges(self.ring_topology_algorithm.graph, edgelist=edge_list, pos=pos
                                   , ax=self.ring_ax, connectionstyle='arc3,rad=0.2'
                                   , arrows=True, edge_color=color)
        self.canvas.draw()
