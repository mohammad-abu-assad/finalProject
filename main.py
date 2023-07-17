from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Online_MINADM_algorithm import online_min_adm_algorithm
from MINADM_analysis import min_adm_analysis
import random as rnd
from experiments_for_the_algorithm import Experiments_for_the_algorithm


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.path_topology_algorithm = online_min_adm_algorithm()
        self.path_topology_algorithm.__init__()
        self.ring_topology_algorithm = online_min_adm_algorithm()
        self.ring_topology_algorithm.__init__()
        self.path_canvas = None
        self.ring_canvas = None
        self.path_ax = None
        self.ring_ax = None

        self.optimal_path_topology_algorithm = online_min_adm_algorithm()
        self.optimal_path_topology_algorithm.__init__()
        self.online_path_topology_algorithm = online_min_adm_algorithm()
        self.online_path_topology_algorithm.__init__()
        self.optimal_ring_topology_algorithm = online_min_adm_algorithm()
        self.optimal_ring_topology_algorithm.__init__()
        self.online_ring_topology_algorithm = online_min_adm_algorithm()
        self.online_ring_topology_algorithm.__init__()

        self.optimal_path_topology_canvas = None
        self.online_path_topology_canvas = None
        self.optimal_ring_topology_canvas = None
        self.online_ring_topology_canvas = None

        self.optimal_path_topology_ax = None
        self.online_path_topology_ax = None
        self.optimal_ring_topology_ax = None
        self.online_ring_topology_ax = None

        self.optimal_ring_topology_pos = None
        self.online_ring_topology_pos = None

        uic.loadUi("main.ui", self)
        self.setWindowTitle("Online-MINADM")
        self.add_light_path_widget_ring = self.findChild(QtWidgets.QWidget, "add_light_path_Widget_ring")
        self.add_light_path_widget_path = self.findChild(QtWidgets.QWidget, "add_light_path_Widget_path")
        self.starting_node_path = self.add_light_path_widget_path.findChild(QtWidgets.QComboBox, "starting_node_path")
        self.starting_node_path.currentTextChanged.connect(self.on_select_starting_path_node)
        self.starting_node_ring = self.add_light_path_widget_ring.findChild(QtWidgets.QComboBox, "starting_node_ring")
        self.starting_node_ring.currentTextChanged.connect(self.on_select_starting_ring_node)
        self.ending_node_path = self.add_light_path_widget_path.findChild(QtWidgets.QComboBox, "ending_node_path")
        self.ending_node_path.currentTextChanged.connect(self.on_select_ending_path_node)
        self.ending_node_ring = self.add_light_path_widget_ring.findChild(QtWidgets.QComboBox, "ending_node_ring")
        self.ending_node_ring.currentTextChanged.connect(self.on_select_ending_ring_node)
        self.add_light_path = self.add_light_path_widget_path.findChild(QtWidgets.QPushButton, "add_light_path")
        self.add_light_path.clicked.connect(self.on_press_add_light_path)
        self.add_light_ring = self.add_light_path_widget_ring.findChild(QtWidgets.QPushButton, "add_light_ring")
        self.add_light_ring.clicked.connect(self.on_press_add_light_ring)

        self.is_long_path = self.add_light_path_widget_ring.findChild(QtWidgets.QCheckBox, "is_long_path")
        self.is_long_path.stateChanged.connect(self.on_check_is_long)
        self.is_long = False

        self.number_of_nodes_in_path_topology = 0
        self.number_of_nodes_in_ring_topology = 0

        self.add_light_path_widget_ring.hide()
        self.add_light_path_widget_path.hide()
        self.select_number_of_nodes_path = self.findChild(QtWidgets.QComboBox, "select_number_of_nodes_path")

        self.select_number_of_nodes_ring = self.findChild(QtWidgets.QComboBox, "select_number_of_nodes_ring")
        self.select_number_of_nodes_path.currentTextChanged.connect(self.on_select_path)
        self.select_number_of_nodes_ring.currentTextChanged.connect(self.on_select_ring)
        self.my_tab = self.findChild(QtWidgets.QTabWidget, "tabWidget")
        self.my_tab.setCurrentIndex(0)
        self.algorithm_simolution_btn = self.findChild(QtWidgets.QPushButton, "algorithm_simolution_btn")
        self.algorithm_analysis_btn = self.findChild(QtWidgets.QPushButton, "algorithm_analysis_btn")
        self.algorithm_simolution_btn.clicked.connect(self.on_algorithm_simolution_btn_clicked)
        self.algorithm_analysis_btn.clicked.connect(self.on_algorithm_analysis_btn_clicked)

        self.optimal_solution_btn = self.findChild(QtWidgets.QPushButton, "optimal_solution_btn")
        self.optimal_solution_btn.clicked.connect(self.on_optimal_solution_btn_clicked)

        self.path_graph_layout = self.findChild(QtWidgets.QVBoxLayout, "path_graph_layout")
        self.ring_graph_layout = self.findChild(QtWidgets.QVBoxLayout, "ring_graph_layout")
        self.path_topology_graph = nx.path_graph(0)
        self.ring_topology_graph = nx.cycle_graph(0)
        self.path_topology_tab = self.my_tab.findChild(QtWidgets.QWidget, "path_topology_tab")
        self.ring_topology_tab = self.my_tab.findChild(QtWidgets.QWidget, "ring_topology_tab")

        self.number_of_nodes_cycle_graph_analysis = self.findChild(QtWidgets.QTextEdit,
                                                                   "number_of_nodes_cycle_graph_analysis")
        self.number_of_paths_cycle_graph_analysis = self.findChild(QtWidgets.QTextEdit,
                                                                   "number_of_paths_cycle_graph_analysis")
        self.create_cycle_graph_btn = self.findChild(QtWidgets.QPushButton, "create_cycle_graph_btn")
        self.cycle_graphs_result_table = self.findChild(QtWidgets.QTableWidget, "cycle_graphs_result_table")
        self.cycle_graph_analysis_layout = self.findChild(QtWidgets.QVBoxLayout, "cycle_graph_analysis_layout")

        self.number_of_nodes_path_graph_analysis = self.findChild(QtWidgets.QTextEdit,
                                                                  "number_of_nodes_path_graph_analysis")
        self.number_of_paths_path_graph_analysis = self.findChild(QtWidgets.QTextEdit,
                                                                  "number_of_paths_path_graph_analysis")
        self.create_path_graph_btn = self.findChild(QtWidgets.QPushButton, "create_path_graph_btn")
        self.path_graphs_result_table = self.findChild(QtWidgets.QTableWidget, "path_graphs_result_table")
        self.path_graph_analysis_layout = self.findChild(QtWidgets.QVBoxLayout, "path_graph_analysis_layout")
        self.number_of_paths_path_graph_analysis.textChanged.connect(self.update_button_state_path)
        self.number_of_paths_cycle_graph_analysis.textChanged.connect(self.update_button_state_ring)
        self.number_of_nodes_path_graph_analysis.textChanged.connect(self.update_button_state_path)
        self.number_of_nodes_cycle_graph_analysis.textChanged.connect(self.update_button_state_ring)
        self.create_path_graph_btn.clicked.connect(self.on_create_path_graph_btn_clicked)
        self.create_cycle_graph_btn.clicked.connect(self.on_create_cycle_graph_btn_clicked)

        self.path_analysis_canvas = None
        self.ring_analysis_canvas = None

        self.path_analysis_ax = None
        self.ring_analysis_ax = None

        self.path_topology_analysis = min_adm_analysis()
        self.path_topology_analysis.__init__()
        self.ring_topology_analysis = min_adm_analysis()
        self.ring_topology_analysis.__init__()

        self.path_draw_level = 1
        self.ring_pos = None

        self.select_number_of_nodes_optimal_path = self.findChild(QtWidgets.QComboBox, "select_number_of_nodes_path_2")
        self.select_number_of_paths_optimal_path = self.findChild(QtWidgets.QComboBox, "select_number_of_paths_path")
        self.create_optimal_path_graph = self.findChild(QtWidgets.QPushButton, "create_path_graph_btn_2")
        self.optimal_path_arrival_label_path = self.findChild(QtWidgets.QLabel, "optimal_path_arrival_label_path")
        self.optimal_path_graph_layout = self.findChild(QtWidgets.QVBoxLayout, "optimal_path_graph_layout")
        self.optimal_path_sol_info_label = self.findChild(QtWidgets.QLabel, "optimal_path_sol_info_label")
        self.online_path_arrival_label_path = self.findChild(QtWidgets.QLabel, "online_path_arrival_label_path")
        self.online_path_graph_layout = self.findChild(QtWidgets.QVBoxLayout, "online_path_graph_layout")
        self.online_path_sol_info_label = self.findChild(QtWidgets.QLabel, "online_path_sol_info_label")
        self.add_path_to_path_graph = self.findChild(QtWidgets.QPushButton, "add_path_to_path_graph")
        self.add_all_paths_to_path_graph = self.findChild(QtWidgets.QPushButton, "add_all_paths_to_path_graph")
        self.restart_the_path_graph = self.findChild(QtWidgets.QPushButton, "restart_the_path_graph")
        self.clear_all_path_graphs = self.findChild(QtWidgets.QPushButton, "clear_all_path_graphs")

        self.select_number_of_nodes_optimal_ring = self.findChild(QtWidgets.QComboBox, "select_number_of_nodes_ring_2")
        self.select_number_of_paths_optimal_ring = self.findChild(QtWidgets.QComboBox, "select_number_of_paths_ring")
        self.create_optimal_ring_graph = self.findChild(QtWidgets.QPushButton, "create_cycle_graph_btn_2")
        self.optimal_path_arrival_label_ring = self.findChild(QtWidgets.QLabel, "optimal_path_arrival_label_ring")
        self.online_path_arrival_label_ring = self.findChild(QtWidgets.QLabel, "online_path_arrival_label_ring")
        self.optimal_ring_sol_info = self.findChild(QtWidgets.QPlainTextEdit, "optimal_ring_sol_info")
        self.online_ring_sol_info = self.findChild(QtWidgets.QPlainTextEdit, "online_ring_sol_info")
        self.optimal_ring_graph_layout = self.findChild(QtWidgets.QVBoxLayout, "optimal_ring_graph_layout")
        self.online_ring_graph_layout = self.findChild(QtWidgets.QVBoxLayout, "online_ring_graph_layout")
        self.add_path_to_ring_graph = self.findChild(QtWidgets.QPushButton, "add_path_to_ring_graph")
        self.add_all_paths_to_ring_graph = self.findChild(QtWidgets.QPushButton, "add_all_paths_to_ring_graph")
        self.restart_the_ring_graph = self.findChild(QtWidgets.QPushButton, "restart_the_ring_graph")
        self.clear_all_ring_graphs = self.findChild(QtWidgets.QPushButton, "clear_all_ring_graphs")

        self.hide_all_path()
        self.hide_all_ring()

        self.select_number_of_paths_optimal_path.currentTextChanged \
            .connect(self.update_create_optimal_path_graph_btn_state)
        self.select_number_of_nodes_optimal_path.currentTextChanged \
            .connect(self.update_create_optimal_path_graph_btn_state)
        self.select_number_of_nodes_optimal_ring.currentTextChanged \
            .connect(self.update_create_optimal_ring_graph_btn_state)
        self.select_number_of_paths_optimal_ring.currentTextChanged \
            .connect(self.update_create_optimal_ring_graph_btn_state)

        self.create_optimal_path_graph.clicked.connect(self.on_create_optimal_path_graph_btn_clicked)
        self.create_optimal_ring_graph.clicked.connect(self.on_create_optimal_ring_graph_btn_clicked)

        self.add_path_to_path_graph.clicked.connect(self.add_path_to_online_path_topology)
        self.add_all_paths_to_path_graph.clicked.connect(self.add_all_paths_to_online_path_topology)
        self.restart_the_path_graph.clicked.connect(self.restart_online_path_graph)
        self.clear_all_path_graphs.clicked.connect(self.clear_all_path_topology)

        self.add_path_to_ring_graph.clicked.connect(self.add_path_to_online_ring_topology)
        self.add_all_paths_to_ring_graph.clicked.connect(self.add_all_paths_to_online_ring_topology)
        self.restart_the_ring_graph.clicked.connect(self.restart_online_ring_graph)
        self.clear_all_ring_graphs.clicked.connect(self.clear_all_ring_topology)

        self.paths_path_topology = list()
        self.paths_ring_topology = list()
        self.next_online_path_topology = 0
        self.next_online_ring_topology = 0
        self.init_path_topology_analysis_canvas()
        self.init_ring_topology_analysis_canvas()

        self.ring_topology_plaintxt = self.findChild(QtWidgets.QPlainTextEdit, "ring_topology_plaintxt")
        self.path_topology_plaintxt = self.findChild(QtWidgets.QPlainTextEdit, "path_topology_plaintxt")
        self.ring_topology_plaintxt.hide()
        self.path_topology_plaintxt.hide()

        self.change_path_ax_to_xyz = self.findChild(QtWidgets.QPushButton, "change_path_ax_to_xyz")
        self.change_path_ax_to_xy = self.findChild(QtWidgets.QPushButton, "change_path_ax_to_xy")
        self.change_path_ax_to_xz = self.findChild(QtWidgets.QPushButton, "change_path_ax_to_xz")
        self.change_path_ax_to_yz = self.findChild(QtWidgets.QPushButton, "change_path_ax_to_yz")

        self.change_ring_ax_to_xyz = self.findChild(QtWidgets.QPushButton, "change_ring_ax_to_xyz")
        self.change_ring_ax_to_xy = self.findChild(QtWidgets.QPushButton, "change_ring_ax_to_xy")
        self.change_ring_ax_to_xz = self.findChild(QtWidgets.QPushButton, "change_ring_ax_to_xz")
        self.change_ring_ax_to_yz = self.findChild(QtWidgets.QPushButton, "change_ring_ax_to_yz")

        self.change_path_ax_to_xyz.clicked.connect(self.on_change_path_ax_to_xyz_clicked)
        self.change_path_ax_to_xy.clicked.connect(self.on_change_path_ax_to_xy_clicked)
        self.change_path_ax_to_xz.clicked.connect(self.on_change_path_ax_to_xz_clicked)
        self.change_path_ax_to_yz.clicked.connect(self.on_change_path_ax_to_yz_clicked)

        self.change_ring_ax_to_xyz.clicked.connect(self.on_change_ring_ax_to_xyz_clicked)
        self.change_ring_ax_to_xy.clicked.connect(self.on_change_ring_ax_to_xy_clicked)
        self.change_ring_ax_to_xz.clicked.connect(self.on_change_ring_ax_to_xz_clicked)
        self.change_ring_ax_to_yz.clicked.connect(self.on_change_ring_ax_to_yz_clicked)

        self.path_analysis_label = self.findChild(QtWidgets.QLabel, "path_analysis_label")
        self.ring_analysis_label = self.findChild(QtWidgets.QLabel, "ring_analysis_label")
        self.path_experiments = Experiments_for_the_algorithm(self.path_analysis_ax, self.path_analysis_canvas, "path")

        self.ring_experiments = Experiments_for_the_algorithm(self.ring_analysis_ax, self.ring_analysis_canvas, "ring")

    def on_change_path_ax_to_xyz_clicked(self):
        self.path_analysis_ax.view_init(elev=0, azim=-45)
        self.path_analysis_canvas.draw()

    def on_change_path_ax_to_xy_clicked(self):
        self.path_analysis_ax.view_init(elev=90, azim=0)
        self.path_analysis_canvas.draw()

    def on_change_path_ax_to_xz_clicked(self):
        self.path_analysis_ax.view_init(elev=0, azim=90)
        self.path_analysis_canvas.draw()

    def on_change_path_ax_to_yz_clicked(self):
        self.path_analysis_ax.view_init(elev=0, azim=180)
        self.path_analysis_canvas.draw()

    def on_change_ring_ax_to_xyz_clicked(self):
        self.ring_analysis_ax.view_init(elev=0, azim=-45)
        self.ring_analysis_canvas.draw()

    def on_change_ring_ax_to_xy_clicked(self):
        self.ring_analysis_ax.view_init(elev=90, azim=0)
        self.ring_analysis_canvas.draw()

    def on_change_ring_ax_to_xz_clicked(self):
        self.ring_analysis_ax.view_init(elev=0, azim=90)
        self.ring_analysis_canvas.draw()

    def on_change_ring_ax_to_yz_clicked(self):
        self.ring_analysis_ax.view_init(elev=0, azim=180)
        self.ring_analysis_canvas.draw()

    def is_file_empty(self, file):
        file.seek(0)  # Ensure we are at the beginning of the file
        first_char = file.read(1)  # Read the first character
        return not first_char

    def read_file(self, file):
        file.seek(0)
        data = []
        for line in file:
            data.append(line.strip())
        return data

    def get_points(self, data):
        points = list()
        for line in data:
            point = line.split(",")
            points.append(point)
        return points

    def init_ring_topology_file(self):

        self.add_points_to_ring_topology_file()

    def init_path_topology_file(self):

        self.add_points_to_path_topology_file()

    def init_ring_topology_analysis_canvas(self):
        fig = plt.figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('number of nodes')
        ax.set_ylabel('number of paths')
        ax.set_zlabel('ratio')
        self.ring_analysis_ax = ax
        self.ring_analysis_canvas = canvas
        file = open("ring_topology_analysis_data.txt", 'r')
        if not self.is_file_empty(file):
            data = self.read_file(file)
            points = self.get_points(data)
            x = [int(point[0]) for point in points]
            y = [int(point[1]) for point in points]
            z = [float(point[2]) for point in points]
            max_z = max(z)
            avg_z = sum(z) / len(z)
            colors = list()
            for i in range(len(z)):
                z1 = z[i]
                if z1 >= 1.3:
                    colors.append("darkred")
                elif z1 >= 1.10:
                    colors.append("red")
                else:
                    colors.append("lightcoral")

            self.ring_analysis_ax.scatter(x, y, z, s=50, c=colors)
            txt = f"max ratio: {round(max_z, 2)}, average ratio: {round(avg_z, 2)}"
            self.ring_analysis_label.setText(txt)
        file.close()
        self.cycle_graph_analysis_layout.addWidget(self.ring_analysis_canvas)

    def init_path_topology_analysis_canvas(self):
        fig = plt.figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('number of nodes')
        ax.set_ylabel('number of paths')
        ax.set_zlabel('ratio')
        self.path_analysis_ax = ax
        self.path_analysis_canvas = canvas
        file = open("path_topology_analysis_data.txt", 'r')
        if not self.is_file_empty(file):
            data = self.read_file(file)
            points = self.get_points(data)
            x = [int(point[0]) for point in points]
            y = [int(point[1]) for point in points]
            z = [float(point[2]) for point in points]
            max_z = max(z)
            avg_z = sum(z) / len(z)
            colors = list()
            for i in range(len(z)):
                z1 = z[i]
                if z1 >= 1.25:
                    colors.append("darkred")
                elif z1 >= 1.10:
                    colors.append("red")
                else:
                    colors.append("lightcoral")

            self.path_analysis_ax.scatter(x, y, z, s=50, c=colors)
            txt = f"max ratio: {round(max_z,2)}, average ratio: {round(avg_z,2)}"
            self.path_analysis_label.setText(txt)
        file.close()
        self.path_graph_analysis_layout.addWidget(self.path_analysis_canvas)

    def clear_all_path_topology(self):
        self.hide_all_path()
        self.optimal_path_topology_canvas.hide()
        self.online_path_topology_canvas.hide()

    def clear_all_ring_topology(self):
        self.hide_all_ring()
        self.optimal_ring_topology_canvas.hide()
        self.online_ring_topology_canvas.hide()

    def on_create_optimal_path_graph_btn_clicked(self):
        number_of_nodes = int(self.select_number_of_nodes_optimal_path.currentText())
        number_of_paths = int(self.select_number_of_paths_optimal_path.currentText())
        self.display_optimal_path_graph(number_of_nodes)
        generate_optimal_paths = min_adm_analysis()
        generate_optimal_paths.__init__()
        generate_optimal_paths.number_of_paths = number_of_paths
        generate_optimal_paths.number_of_nodes = number_of_nodes
        generate_optimal_paths.create_paths_for_path_topology()
        paths = generate_optimal_paths.paths
        self.paths_path_topology = paths
        self.display_path_labels()
        count = 1
        for path in paths:
            s = self.optimal_path_arrival_label_path.text()
            self.optimal_path_arrival_label_path.setText(f"{s} Path {count} arrives: {path},")
            self.add_light_path_to_optimal_path_topology(path)
            self.optimal_path_sol_info_label.setText(
                f"The solution is {self.optimal_path_topology_algorithm.solution()}"
                f", total ADMs= {sum(self.optimal_path_topology_algorithm.adm)} ")
            count += 1
            self.repaint()

        rnd.shuffle(self.paths_path_topology)
        self.display_online_path_graph(number_of_nodes)
        self.show_path_topology_buttons()
        self.set_enable_path_topology_buttons(True)

    def add_path_to_online_path_topology(self):
        if self.next_online_path_topology >= len(self.paths_path_topology):
            return
        i = self.next_online_path_topology
        path = self.paths_path_topology[i]
        self.online_path_arrival_label_path.setText(f"Path {i + 1} arrives: {path},")
        self.add_light_path_to_online_path_topology(path)
        self.online_path_sol_info_label.setText(
            f"The solution is {self.online_path_topology_algorithm.solution()}"
            f", total ADMs= {sum(self.online_path_topology_algorithm.adm)} ")
        if self.next_online_path_topology == len(self.paths_path_topology) - 1:
            cr = sum(self.online_path_topology_algorithm.adm) / sum(self.optimal_path_topology_algorithm.adm)
            text = self.online_path_sol_info_label.text()
            self.online_path_sol_info_label.setText(f"{text}, competitive ratio= {round(cr, 2)}")
        self.next_online_path_topology += 1

    def add_all_paths_to_online_path_topology(self):
        self.restart_online_path_graph()
        paths = self.paths_path_topology
        rnd.shuffle(paths)
        count = 1
        for path in paths:
            self.online_path_arrival_label_path.setText(f"Path {count} arrives: {path},")
            self.add_light_path_to_online_path_topology(path)
            self.online_path_sol_info_label.setText(
                f"The solution is {self.online_path_topology_algorithm.solution()}"
                f", total ADMs= {sum(self.online_path_topology_algorithm.adm)} ")
            count += 1
        cr = sum(self.online_path_topology_algorithm.adm) / sum(self.optimal_path_topology_algorithm.adm)
        text = self.online_path_sol_info_label.text()
        self.online_path_sol_info_label.setText(f"{text}, competitive ratio= {round(cr, 2)}")
        self.next_online_path_topology = len(paths)

    def restart_online_path_graph(self):
        self.display_online_path_graph(int(self.select_number_of_nodes_optimal_path.currentText()))
        rnd.shuffle(self.paths_path_topology)
        self.next_online_path_topology = 0
        self.online_path_arrival_label_path.setText("")
        self.online_path_sol_info_label.setText("")

    def display_path_labels(self):
        self.optimal_path_sol_info_label.show()
        self.optimal_path_sol_info_label.setText("")
        self.online_path_arrival_label_path.show()
        self.online_path_arrival_label_path.setText("")
        self.optimal_path_arrival_label_path.show()
        self.optimal_path_arrival_label_path.setText("")
        self.online_path_sol_info_label.show()
        self.online_path_sol_info_label.setText("")

    def display_ring_labels(self):
        self.optimal_ring_sol_info.show()
        self.optimal_ring_sol_info.setPlainText("")
        self.optimal_path_arrival_label_ring.show()
        self.optimal_path_arrival_label_ring.setText("")
        self.online_ring_sol_info.show()
        self.online_ring_sol_info.setPlainText("")
        self.online_path_arrival_label_ring.show()
        self.online_path_arrival_label_ring.setText("")

    def on_create_optimal_ring_graph_btn_clicked(self):
        number_of_nodes = int(self.select_number_of_nodes_optimal_ring.currentText())
        number_of_paths = int(self.select_number_of_paths_optimal_ring.currentText())
        self.display_optimal_ring_topology_graph(number_of_nodes)
        generate_optimal_paths = min_adm_analysis()
        generate_optimal_paths.__init__()
        generate_optimal_paths.number_of_paths = number_of_paths
        generate_optimal_paths.number_of_nodes = number_of_nodes
        generate_optimal_paths.create_paths_for_ring_topology()
        paths = generate_optimal_paths.paths
        self.paths_ring_topology = paths
        self.display_ring_labels()
        for path in paths:
            self.optimal_path_arrival_label_ring.setText(f"Paths : {paths},")
            self.add_light_path_to_optimal_ring_topology(path)
            self.optimal_ring_sol_info.setPlainText(
                f"The solution is {self.optimal_ring_topology_algorithm.solution()}"
                f",\ntotal ADMs= {sum(self.optimal_ring_topology_algorithm.adm)} ")

        rnd.shuffle(self.paths_ring_topology)
        self.display_online_ring_topology_graph(number_of_nodes)
        self.show_ring_topology_buttons()
        self.set_enable_ring_topology_buttons(True)

    def add_path_to_online_ring_topology(self):
        if self.next_online_ring_topology >= len(self.paths_ring_topology):
            return
        i = self.next_online_ring_topology
        path = self.paths_ring_topology[i]
        self.online_path_arrival_label_ring.setText(f"Path {i + 1} arrives: {path},")
        self.add_light_path_to_online_ring_topology(path)
        self.online_ring_sol_info.setPlainText(
            f"The solution is {self.online_ring_topology_algorithm.solution()}"
            f",\ntotal ADMs= {sum(self.online_ring_topology_algorithm.adm)} ")
        if self.next_online_ring_topology == len(self.paths_ring_topology) - 1:
            cr = sum(self.online_ring_topology_algorithm.adm) / sum(self.optimal_ring_topology_algorithm.adm)
            text = self.online_ring_sol_info.toPlainText()
            self.online_ring_sol_info.setPlainText(f"{text}, competitive ratio= {round(cr, 2)}")
        self.next_online_ring_topology += 1

    def add_all_paths_to_online_ring_topology(self):
        self.restart_online_ring_graph()
        paths = self.paths_ring_topology
        rnd.shuffle(paths)
        self.online_path_arrival_label_ring.setText(f"Paths: {paths}")
        for path in paths:
            self.add_light_path_to_online_ring_topology(path)
            self.online_ring_sol_info.setPlainText(
                f"The solution is {self.online_ring_topology_algorithm.solution()}"
                f",\ntotal ADMs= {sum(self.online_ring_topology_algorithm.adm)} ")
        cr = sum(self.online_ring_topology_algorithm.adm) / sum(self.optimal_ring_topology_algorithm.adm)
        text = self.online_ring_sol_info.toPlainText()
        self.online_ring_sol_info.setPlainText(f"{text}, competitive ratio= {round(cr, 2)}")
        self.next_online_ring_topology = len(paths)

    def restart_online_ring_graph(self):
        self.display_online_ring_topology_graph(int(self.select_number_of_nodes_optimal_ring.currentText()))
        rnd.shuffle(self.paths_ring_topology)
        self.next_online_ring_topology = 0
        self.online_path_arrival_label_ring.setText("")
        self.online_ring_sol_info.setPlainText("")

    def show_ring_topology_buttons(self):
        self.add_path_to_ring_graph.show()
        self.add_all_paths_to_ring_graph.show()
        self.restart_the_ring_graph.show()
        self.clear_all_ring_graphs.show()

    def show_path_topology_buttons(self):
        self.add_path_to_path_graph.show()
        self.add_all_paths_to_path_graph.show()
        self.restart_the_path_graph.show()
        self.clear_all_path_graphs.show()

    def set_enable_ring_topology_buttons(self, is_enabled):
        self.add_path_to_ring_graph.setEnabled(is_enabled)
        self.add_all_paths_to_ring_graph.setEnabled(is_enabled)
        self.restart_the_ring_graph.setEnabled(is_enabled)
        self.clear_all_ring_graphs.setEnabled(is_enabled)

    def set_enable_path_topology_buttons(self, is_enabled):
        self.add_path_to_path_graph.setEnabled(is_enabled)
        self.add_all_paths_to_path_graph.setEnabled(is_enabled)
        self.restart_the_path_graph.setEnabled(is_enabled)
        self.clear_all_path_graphs.setEnabled(is_enabled)

    def update_create_optimal_path_graph_btn_state(self):
        if self.select_number_of_nodes_optimal_path.currentText() == "number of nodes":
            self.create_optimal_path_graph.setEnabled(False)
            return
        if self.select_number_of_paths_optimal_path.currentText() == "number of paths":
            self.create_optimal_path_graph.setEnabled(False)
            return
        self.create_optimal_path_graph.setEnabled(True)

    def update_create_optimal_ring_graph_btn_state(self):
        if self.select_number_of_nodes_optimal_ring.currentText() == "number of nodes":
            self.create_optimal_ring_graph.setEnabled(False)
            return
        if self.select_number_of_paths_optimal_ring.currentText() == "number of paths":
            self.create_optimal_ring_graph.setEnabled(False)
            return
        self.create_optimal_ring_graph.setEnabled(True)

    def hide_all_path(self):
        self.optimal_path_arrival_label_path.hide()
        self.optimal_path_sol_info_label.hide()
        self.online_path_arrival_label_path.hide()
        self.online_path_sol_info_label.hide()
        self.add_path_to_path_graph.hide()
        self.add_all_paths_to_path_graph.hide()
        self.restart_the_path_graph.hide()
        self.clear_all_path_graphs.hide()

    def hide_all_ring(self):
        self.optimal_path_arrival_label_ring.hide()
        self.online_path_arrival_label_ring.hide()
        self.optimal_ring_sol_info.hide()
        self.online_ring_sol_info.hide()
        self.add_path_to_ring_graph.hide()
        self.add_all_paths_to_ring_graph.hide()
        self.restart_the_ring_graph.hide()
        self.clear_all_ring_graphs.hide()

    def add_points_to_ring_topology_file(self):
        for number_of_nodes in range(10, 101, 10):
            f = number_of_nodes // 2
            t = number_of_nodes * 2
            for number_of_paths in range(f, t + 1, 5):
                self.ring_topology_analysis.__init__()
                self.ring_topology_analysis.start_analysis(number_of_nodes, number_of_paths, 'r')
                competitive_ratio = self.ring_topology_analysis.competitive_ratio
                line = f"{number_of_nodes},{number_of_paths},{competitive_ratio}\n"
                with open("ring_topology_analysis_data.txt", 'a') as file:
                    file.write(line)
                x = number_of_nodes
                y = number_of_paths
                z = competitive_ratio
                self.ring_analysis_ax.scatter(x, y, z, s=50, c='red')
                self.ring_analysis_canvas.draw()

    def add_points_to_path_topology_file(self):
        for number_of_nodes in range(10, 101, 10):
            f = number_of_nodes // 2
            t = number_of_nodes * 2
            for number_of_paths in range(f, t + 1, 5):
                self.path_topology_analysis.__init__()
                self.path_topology_analysis.start_analysis(number_of_nodes, number_of_paths, 'p')
                competitive_ratio = self.path_topology_analysis.competitive_ratio
                line = f"{number_of_nodes},{number_of_paths},{competitive_ratio}\n"
                with open("path_topology_analysis_data.txt", 'a') as file:
                    file.write(line)
                x = number_of_nodes
                y = number_of_paths
                z = competitive_ratio
                self.path_analysis_ax.scatter(x, y, z, s=50, c='red')
                self.path_analysis_canvas.draw()

    def on_create_path_graph_btn_clicked(self):
        if not self.create_path_graph_btn.isEnabled():
            return
        number_of_nodes = int(self.number_of_nodes_path_graph_analysis.toPlainText().strip())
        number_of_paths = int(self.number_of_paths_path_graph_analysis.toPlainText().strip())
        self.path_topology_analysis.__init__()
        self.path_topology_analysis.start_analysis(number_of_nodes, number_of_paths, 'p')
        competitive_ratio = self.path_topology_analysis.competitive_ratio
        line = f"{number_of_nodes},{number_of_paths},{competitive_ratio}\n"
        with open("path_topology_analysis_data.txt", 'a') as file:
            file.write(line)
        x = number_of_nodes
        y = number_of_paths
        z = competitive_ratio
        file = open("path_topology_analysis_data.txt", 'r')
        if not self.is_file_empty(file):
            data = self.read_file(file)
            points = self.get_points(data)
            z1 = [float(point[2]) for point in points]
            max_z = max(z1)
            avg_z = sum(z1) / len(z1)
            if competitive_ratio >= 1.25:
                self.path_analysis_ax.scatter(x, y, z, s=50, c="darkred")
            elif competitive_ratio >= 1.10:
                self.path_analysis_ax.scatter(x, y, z, s=50, c='red')
            else:
                self.path_analysis_ax.scatter(x, y, z, s=50, c="lightcoral")

            txt = f"max ratio: {round(max_z, 2)}, average ratio: {round(avg_z, 2)}"
            self.path_analysis_label.setText(txt)
        else:
            self.path_analysis_ax.scatter(x, y, z, s=50, c='red')

        self.path_analysis_canvas.draw()
        self.add_new_row_to_path_graphs_table(number_of_nodes, number_of_paths, round(competitive_ratio, 3))

    def on_create_cycle_graph_btn_clicked(self):
        if not self.create_cycle_graph_btn.isEnabled():
            return
        number_of_nodes = int(self.number_of_nodes_cycle_graph_analysis.toPlainText().strip())
        number_of_paths = int(self.number_of_paths_cycle_graph_analysis.toPlainText().strip())
        self.ring_topology_analysis.__init__()
        self.ring_topology_analysis.start_analysis(number_of_nodes, number_of_paths, 'r')
        competitive_ratio = self.ring_topology_analysis.competitive_ratio
        line = f"{number_of_nodes},{number_of_paths},{competitive_ratio}\n"
        with open("ring_topology_analysis_data.txt", 'a') as file:
            file.write(line)
        x = number_of_nodes
        y = number_of_paths
        z = competitive_ratio

        file = open("ring_topology_analysis_data.txt", 'r')
        if not self.is_file_empty(file):
            data = self.read_file(file)
            points = self.get_points(data)
            z1 = [float(point[2]) for point in points]
            max_z = max(z1)
            avg_z = sum(z1) / len(z1)
            if competitive_ratio >= 1.3:
                self.ring_analysis_ax.scatter(x, y, z, s=50, c="#550000")
            elif competitive_ratio >= 1.10:
                self.ring_analysis_ax.scatter(x, y, z, s=50, c='red')
            else:
                self.ring_analysis_ax.scatter(x, y, z, s=50, c="#FF9999")
            txt = f"max ratio: {round(max_z, 2)}, average ratio: {round(avg_z, 2)}"
            self.ring_analysis_label.setText(txt)
        else:
            self.ring_analysis_ax.scatter(x, y, z, s=50, c='red')
        file.close()
        self.ring_analysis_canvas.draw()
        self.add_new_row_to_cycle_graphs_table(number_of_nodes, number_of_paths, round(competitive_ratio, 3))

    def add_new_row_to_path_graphs_table(self, number_of_nodes, number_of_paths, competitive_ratio):
        self.number_of_nodes_path_graph_analysis.clear()
        self.number_of_paths_path_graph_analysis.clear()
        self.path_graphs_result_table.insertRow(0)
        c1 = QtWidgets.QTableWidgetItem(str(number_of_nodes))
        c2 = QtWidgets.QTableWidgetItem(str(number_of_paths))
        c3 = QtWidgets.QTableWidgetItem(str(competitive_ratio))
        self.path_graphs_result_table.setItem(0, 0, c1)
        self.path_graphs_result_table.setItem(0, 1, c2)
        self.path_graphs_result_table.setItem(0, 2, c3)

    def add_new_row_to_cycle_graphs_table(self, number_of_nodes, number_of_paths, competitive_ratio):
        self.number_of_nodes_cycle_graph_analysis.clear()
        self.number_of_paths_cycle_graph_analysis.clear()
        self.cycle_graphs_result_table.insertRow(0)
        c1 = QtWidgets.QTableWidgetItem(str(number_of_nodes))
        c2 = QtWidgets.QTableWidgetItem(str(number_of_paths))
        c3 = QtWidgets.QTableWidgetItem(str(competitive_ratio))
        self.cycle_graphs_result_table.setItem(0, 0, c1)
        self.cycle_graphs_result_table.setItem(0, 1, c2)
        self.cycle_graphs_result_table.setItem(0, 2, c3)
        pass

    def update_button_state_path(self):
        text1 = self.number_of_nodes_path_graph_analysis.toPlainText().strip()
        text2 = self.number_of_paths_path_graph_analysis.toPlainText().strip()
        self.create_path_graph_btn.setEnabled(bool(text1) and bool(text2))

    def update_button_state_ring(self):
        text1 = self.number_of_nodes_cycle_graph_analysis.toPlainText().strip()
        text2 = self.number_of_paths_cycle_graph_analysis.toPlainText().strip()
        self.create_cycle_graph_btn.setEnabled(bool(text1) and bool(text2))

    def on_algorithm_simolution_btn_clicked(self):
        self.my_tab.setCurrentIndex(1)

    def on_algorithm_analysis_btn_clicked(self):
        self.my_tab.setCurrentIndex(2)

    def on_optimal_solution_btn_clicked(self):
        self.my_tab.setCurrentIndex(3)

    def on_select_path(self):
        self.ending_node_path.setEnabled(False)
        self.add_light_path.setEnabled(False)
        self.starting_node_path.clear()
        self.starting_node_path.addItem("starting node")
        if self.select_number_of_nodes_path.currentText() == "number of nodes":
            self.add_light_path_widget_path.hide()
            self.path_canvas.hide()
            self.path_topology_plaintxt.hide()
            return

        self.add_light_path_widget_path.show()
        selected = int(self.select_number_of_nodes_path.currentText())
        self.number_of_nodes_in_path_topology = selected
        self.display_path_topology_graph(selected)
        items = []
        for i in range(1, selected + 1):
            items.append(str(i))
        self.starting_node_path.addItems(items)

    def on_select_ring(self):
        self.ending_node_ring.setEnabled(False)
        self.add_light_ring.setEnabled(False)
        self.is_long_path.setEnabled(False)
        self.starting_node_ring.clear()
        self.starting_node_ring.addItem("starting node")

        if self.select_number_of_nodes_ring.currentText() == "number of nodes":
            self.add_light_path_widget_ring.hide()
            self.ring_canvas.hide()
            self.ring_topology_plaintxt.hide()
            return

        self.add_light_path_widget_ring.show()

        selected = int(self.select_number_of_nodes_ring.currentText())

        self.number_of_nodes_in_ring_topology = selected
        self.display_ring_topology_graph(selected)
        items = []
        for i in range(1, selected + 1):
            items.append(str(i))
        self.starting_node_ring.addItems(items)

    def on_select_starting_path_node(self):
        self.add_light_path.setEnabled(False)
        self.ending_node_path.clear()
        self.ending_node_path.addItem("ending node")
        if self.starting_node_path.currentText() == "":
            return
        if self.starting_node_path.currentText() == "starting node":
            self.ending_node_path.setEnabled(False)
            return

        self.ending_node_path.setEnabled(True)
        selected = int(self.starting_node_path.currentText())
        items = []
        for i in range(1, self.number_of_nodes_in_path_topology + 1):
            if i == selected:
                pass
            else:
                items.append(str(i))
        self.ending_node_path.addItems(items)

    def on_select_starting_ring_node(self):
        self.add_light_ring.setEnabled(False)
        self.is_long_path.setEnabled(False)
        self.ending_node_ring.clear()
        self.ending_node_ring.addItem("ending node")
        if self.starting_node_ring.currentText() == "":
            return
        if self.starting_node_ring.currentText() == "starting node":
            self.ending_node_ring.setEnabled(False)
            return

        self.ending_node_ring.setEnabled(True)
        selected = int(self.starting_node_ring.currentText())
        items = []
        for i in range(1, self.number_of_nodes_in_ring_topology + 1):
            items.append(str(i))
        self.ending_node_ring.addItems(items)

    def on_select_ending_path_node(self):
        if self.ending_node_path.currentText() == "":
            return
        if self.ending_node_path.currentText() == "ending node":
            self.add_light_path.setEnabled(False)
            return
        self.add_light_path.setEnabled(True)

    def on_select_ending_ring_node(self):
        if self.ending_node_ring.currentText() == "":
            return
        if self.ending_node_ring.currentText() == "ending node":
            self.add_light_ring.setEnabled(False)
            self.is_long_path.setEnabled(False)
            return

        self.is_long_path.setChecked(False)
        self.add_light_ring.setEnabled(True)
        self.is_long_path.setEnabled(True)
        if self.ending_node_ring.currentText() == self.starting_node_ring.currentText():
            self.is_long_path.setChecked(True)
            self.is_long_path.setEnabled(False)

    def on_press_add_light_path(self):
        start_node = int(self.starting_node_path.currentText())
        end_node = int(self.ending_node_path.currentText())
        if start_node > end_node:
            start_node, end_node = end_node, start_node
        path = list(range(start_node, end_node + 1))
        self.path_topology_algorithm.add_light_path(path)
        starting_node = self.path_topology_algorithm.paths[-1][0]
        ending_node = self.path_topology_algorithm.paths[-1][-1]
        color = self.path_topology_algorithm.path_colour[-1]
        for i in range(len(self.path_topology_algorithm.colours)):
            if self.path_topology_algorithm.colours[i] == color:
                index = i
                break
        # self.path_ax.axhline(y=index+1, xmin=starting_node, xmax=ending_node-0.1, color=color)
        self.path_ax.plot([starting_node, ending_node - 0.1], [index + 1, index + 1], color=color)
        print(f"new path added: {path}")
        print(f"color: {color}")
        txt = f"new path added: {path}\n" \
              f"new path's color: {color}\n" \
              f"total ADMs: {sum(self.path_topology_algorithm.adm)}"
        self.path_topology_plaintxt.setPlainText(txt)
        self.path_canvas.draw()

        # nx.draw_networkx(self.path_topology_graph, ax=ax)

    def add_light_path_to_online_path_topology(self, path):
        self.online_path_topology_algorithm.add_light_path(path)
        starting_node = self.online_path_topology_algorithm.paths[-1][0]
        ending_node = self.online_path_topology_algorithm.paths[-1][-1]
        color = self.online_path_topology_algorithm.path_colour[-1]
        for i in range(len(self.online_path_topology_algorithm.colours)):
            if self.online_path_topology_algorithm.colours[i] == color:
                index = i
                break
        self.online_path_topology_ax.plot([starting_node, ending_node - 0.1], [index + 1, index + 1], color=color)
        self.online_path_topology_canvas.draw()
        self.online_path_graph_layout.update()

    def add_light_path_to_optimal_path_topology(self, path):
        self.optimal_path_topology_algorithm.add_light_path(path)
        starting_node = self.optimal_path_topology_algorithm.paths[-1][0]
        ending_node = self.optimal_path_topology_algorithm.paths[-1][-1]
        color = self.optimal_path_topology_algorithm.path_colour[-1]
        for i in range(len(self.optimal_path_topology_algorithm.colours)):
            if self.optimal_path_topology_algorithm.colours[i] == color:
                index = i
                break
        # self.path_ax.axhline(y=index+1, xmin=starting_node, xmax=ending_node-0.1, color=color)
        self.optimal_path_topology_ax.plot([starting_node, ending_node - 0.1], [index + 1, index + 1], color=color)
        self.optimal_path_topology_canvas.draw()
        self.optimal_path_graph_layout.update()

    def list_in_clockwise_order(self, start, end):
        number_of_nodes = self.number_of_nodes_in_ring_topology
        if start < end:
            clockwise_list = list(range(start, end + 1))
        else:
            clockwise_list = list(range(start, number_of_nodes + 1)) + list(range(1, end + 1))
        return clockwise_list

    def on_press_add_light_ring(self):
        start_node = int(self.starting_node_ring.currentText())
        end_node = int(self.ending_node_ring.currentText())
        if self.is_long_path.isChecked():
            start_node, end_node = end_node, start_node
        self.ring_topology_algorithm.add_light_path(self.list_in_clockwise_order(start_node, end_node))
        path = self.ring_topology_algorithm.paths[-1]
        color = self.ring_topology_algorithm.path_colour[-1]
        for i in range(len(self.ring_topology_algorithm.colours)):
            if self.ring_topology_algorithm.colours[i] == color:
                index = i
                break
        pos = nx.circular_layout(self.ring_topology_algorithm.graph, scale=2.5 + 0.5 * index)
        edge_list = list()
        for i in range(len(path) - 1):
            edge_list.append((path[i], path[i + 1]))
        nx.draw_networkx_edges(self.ring_topology_algorithm.graph, edgelist=edge_list, pos=pos
                               , ax=self.ring_ax, connectionstyle='arc3,rad=0.2'
                               , arrows=True, edge_color=color)
        txt = f"new path added: {path}\n" \
              f"new path's color: {color}\n" \
              f"total ADMs: {sum(self.ring_topology_algorithm.adm)}"
        self.ring_topology_plaintxt.setPlainText(txt)
        self.ring_canvas.draw()
        self.repaint()

    def add_light_path_to_optimal_ring_topology(self, path):
        self.optimal_ring_topology_algorithm.add_light_path(path)
        color = self.optimal_ring_topology_algorithm.path_colour[-1]
        for i in range(len(self.optimal_ring_topology_algorithm.colours)):
            if self.optimal_ring_topology_algorithm.colours[i] == color:
                index = i
                break
        pos = nx.circular_layout(self.optimal_ring_topology_algorithm.graph, scale=2.5 + 0.5 * index)
        edge_list = list()
        for i in range(len(path) - 1):
            edge_list.append((path[i], path[i + 1]))
        nx.draw_networkx_edges(self.optimal_ring_topology_algorithm.graph, edgelist=edge_list, pos=pos
                               , ax=self.optimal_ring_topology_ax, connectionstyle='arc3,rad=0.2'
                               , arrows=True, edge_color=color)

        self.optimal_ring_topology_canvas.draw()
        self.repaint()

    def add_light_path_to_online_ring_topology(self, path):
        self.online_ring_topology_algorithm.add_light_path(path)
        color = self.online_ring_topology_algorithm.path_colour[-1]
        for i in range(len(self.online_ring_topology_algorithm.colours)):
            if self.online_ring_topology_algorithm.colours[i] == color:
                index = i
                break
        pos = nx.circular_layout(self.online_ring_topology_algorithm.graph, scale=2.5 + 0.5 * index)
        edge_list = list()
        for i in range(len(path) - 1):
            edge_list.append((path[i], path[i + 1]))
        nx.draw_networkx_edges(self.online_ring_topology_algorithm.graph, edgelist=edge_list, pos=pos
                               , ax=self.online_ring_topology_ax, connectionstyle='arc3,rad=0.2'
                               , arrows=True, edge_color=color)

        self.online_ring_topology_canvas.draw()
        self.repaint()

    def on_check_is_long(self):
        self.is_long = self.is_long_path.isChecked()

    def display_path_topology_graph(self, number_of_nodes):
        self.path_topology_algorithm.__init__()
        self.path_topology_algorithm.create_path_graph(number_of_nodes)
        fig = plt.figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        self.path_ax = ax
        ax.axis('off')
        pos = {node: (node, 0) for node in self.path_topology_algorithm.graph.nodes}

        nx.draw_networkx(self.path_topology_algorithm.graph, ax=ax, pos=pos, node_size=500)
        self.path_canvas = canvas
        while self.path_graph_layout.count():
            item = self.path_graph_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.path_topology_plaintxt.show()
        self.path_topology_plaintxt.setPlainText("add light paths to see results.")
        self.path_graph_layout.addWidget(canvas)

    def display_optimal_path_graph(self, number_of_nodes):
        self.optimal_path_topology_algorithm.__init__()
        self.optimal_path_topology_algorithm.create_path_graph(number_of_nodes)
        fig = plt.figure()
        canvas = FigureCanvas(fig)
        self.optimal_path_topology_canvas = canvas
        ax = fig.add_subplot(111)
        ax.axis('off')
        self.optimal_path_topology_ax = ax
        pos = {node: (node, 0) for node in self.optimal_path_topology_algorithm.graph.nodes}

        nx.draw_networkx(self.optimal_path_topology_algorithm.graph, ax=ax, pos=pos, node_size=500)

        while self.optimal_path_graph_layout.count():
            item = self.optimal_path_graph_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.optimal_path_graph_layout.addWidget(canvas)
        canvas.draw()
        self.repaint()

    def display_online_path_graph(self, number_of_nodes):
        self.online_path_topology_algorithm.__init__()
        self.online_path_topology_algorithm.create_path_graph(number_of_nodes)
        fig = plt.figure()
        canvas = FigureCanvas(fig)
        self.online_path_topology_canvas = canvas
        ax = fig.add_subplot(111)
        ax.axis('off')
        self.online_path_topology_ax = ax
        pos = {node: (node, 0) for node in self.online_path_topology_algorithm.graph.nodes}

        nx.draw_networkx(self.online_path_topology_algorithm.graph, ax=ax, pos=pos, node_size=500)
        while self.online_path_graph_layout.count():
            item = self.online_path_graph_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.online_path_graph_layout.addWidget(canvas)

    def display_ring_topology_graph(self, number_of_nodes):
        self.ring_topology_algorithm.__init__()
        self.ring_topology_algorithm.create_cycle_graph(number_of_nodes)
        # self.ring_topology_graph = nx.cycle_graph(number_of_nodes)
        # self.ring_topology_graph = nx.relabel_nodes(self.ring_topology_graph,
        #                                            {i: i + 1 for i in range(number_of_nodes)})
        # Create a Matplotlib figure and add the NetworkX graph to it
        fig = plt.figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        self.ring_ax = ax
        ax.axis('off')

        pos = nx.circular_layout(self.ring_topology_algorithm.graph, scale=2.0)

        self.ring_pos = pos
        # nx.draw_networkx(self.ring_topology_algorithm.graph, ax=ax, with_labels=True, node_size=1000, pos=pos)
        nx.draw_networkx_nodes(self.ring_topology_algorithm.graph, pos=pos, ax=ax, node_size=500)
        edge_list = list()
        for i in range(number_of_nodes - 1):
            edge_list.append((i + 1, i + 2))
        nx.draw_networkx_edges(self.ring_topology_algorithm.graph, edgelist=edge_list, pos=pos
                               , ax=ax, connectionstyle='arc3,rad=0.2'
                               , arrows=True)

        nx.draw_networkx_edges(self.ring_topology_algorithm.graph, edgelist=[(number_of_nodes, 1)], pos=pos
                               , ax=ax, connectionstyle='arc3,rad=0.2'
                               , arrows=True)

        nx.draw_networkx_labels(self.ring_topology_algorithm.graph, pos, ax=ax)
        ax.set_aspect('equal')
        # nx.draw_networkx(self.ring_topology_graph, ax=ax)
        self.ring_canvas = canvas
        while self.ring_graph_layout.count():
            item = self.ring_graph_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.ring_topology_plaintxt.show()
        self.ring_topology_plaintxt.setPlainText("add light paths to see results")
        self.ring_graph_layout.addWidget(self.ring_canvas)

    def display_optimal_ring_topology_graph(self, number_of_nodes):
        self.optimal_ring_topology_algorithm.__init__()
        self.optimal_ring_topology_algorithm.create_cycle_graph(number_of_nodes)
        fig = plt.figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        self.optimal_ring_topology_ax = ax
        ax.axis('off')

        pos = nx.circular_layout(self.optimal_ring_topology_algorithm.graph, scale=2.0)

        self.optimal_ring_topology_pos = pos
        # nx.draw_networkx(self.ring_topology_algorithm.graph, ax=ax, with_labels=True, node_size=1000, pos=pos)
        nx.draw_networkx_nodes(self.optimal_ring_topology_algorithm.graph, pos=pos, ax=ax, node_size=500)
        edge_list = list()
        for i in range(number_of_nodes - 1):
            edge_list.append((i + 1, i + 2))
        nx.draw_networkx_edges(self.optimal_ring_topology_algorithm.graph, edgelist=edge_list, pos=pos
                               , ax=ax, connectionstyle='arc3,rad=0.2'
                               , arrows=True)

        nx.draw_networkx_edges(self.optimal_ring_topology_algorithm.graph, edgelist=[(number_of_nodes, 1)], pos=pos
                               , ax=ax, connectionstyle='arc3,rad=0.2'
                               , arrows=True)

        nx.draw_networkx_labels(self.optimal_ring_topology_algorithm.graph, pos, ax=ax)
        ax.set_aspect('equal')
        # nx.draw_networkx(self.ring_topology_graph, ax=ax)
        self.optimal_ring_topology_canvas = canvas
        while self.optimal_ring_graph_layout.count():
            item = self.optimal_ring_graph_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.optimal_ring_graph_layout.addWidget(self.optimal_ring_topology_canvas)

    def display_online_ring_topology_graph(self, number_of_nodes):
        self.online_ring_topology_algorithm.__init__()
        self.online_ring_topology_algorithm.create_cycle_graph(number_of_nodes)
        fig = plt.figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        self.online_ring_topology_ax = ax
        ax.axis('off')

        pos = nx.circular_layout(self.online_ring_topology_algorithm.graph, scale=2.0)

        self.online_ring_topology_pos = pos
        # nx.draw_networkx(self.ring_topology_algorithm.graph, ax=ax, with_labels=True, node_size=1000, pos=pos)
        nx.draw_networkx_nodes(self.online_ring_topology_algorithm.graph, pos=pos, ax=ax, node_size=500)
        edge_list = list()
        for i in range(number_of_nodes - 1):
            edge_list.append((i + 1, i + 2))
        nx.draw_networkx_edges(self.online_ring_topology_algorithm.graph, edgelist=edge_list, pos=pos
                               , ax=ax, connectionstyle='arc3,rad=0.2'
                               , arrows=True)

        nx.draw_networkx_edges(self.online_ring_topology_algorithm.graph, edgelist=[(number_of_nodes, 1)], pos=pos
                               , ax=ax, connectionstyle='arc3,rad=0.2'
                               , arrows=True)

        nx.draw_networkx_labels(self.online_ring_topology_algorithm.graph, pos, ax=ax)
        ax.set_aspect('equal')
        # nx.draw_networkx(self.ring_topology_graph, ax=ax)
        self.online_ring_topology_canvas = canvas
        while self.online_ring_graph_layout.count():
            item = self.online_ring_graph_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.online_ring_graph_layout.addWidget(self.online_ring_topology_canvas)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindow()
    # MainWindow.ring_experiments.start_experiments()
    # MainWindow.__init__()
    # MainWindow.init_ring_topology_file()
    MainWindow.show()
    sys.exit(app.exec_())
