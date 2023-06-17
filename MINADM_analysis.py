import networkx as nx
from Online_MINADM_algorithm import online_min_adm_algorithm
import random as rnd


class min_adm_analysis:
    def __init__(self):
        self.optimal_min_adm = online_min_adm_algorithm()
        self.optimal_min_adm.__init__()
        self.online_min_adm = online_min_adm_algorithm()
        self.online_min_adm.__init__()
        self.number_of_nodes = 0
        self.number_of_paths = 0
        self.ring_or_path = ''
        self.paths = []
        self.optimal_sol = 0
        self.online_sol = 0
        self.competitive_ratio = 0

    def start_analysis(self, number_of_nodes, number_of_paths, ring_or_path):
        self.number_of_nodes = number_of_nodes
        self.number_of_paths = number_of_paths
        self.ring_or_path = ring_or_path
        self.paths.clear()
        self.online_min_adm.clear_algorithm()
        self.optimal_min_adm.clear_algorithm()
        if self.ring_or_path == 'p':
            self.start_analysis_for_path_topology()
        else:
            self.start_analysis_for_ring_topology()
        self.calculate_optimal_sol()
        ratio_sum = 0
        for i in range(10):
            self.calculate_random_sol()
            ratio = self.online_sol / self.optimal_sol
            ratio_sum += ratio
        avg = ratio_sum / 10
        # self.calculate_random_sol()
        # if self.optimal_sol != 0:
        #   if self.optimal_sol > self.online_sol:
        #        self.optimal_sol, self.online_sol = self.online_sol, self.optimal_sol
        self.competitive_ratio = avg

    def start_analysis_for_path_topology(self):
        self.optimal_min_adm.create_path_graph(self.number_of_nodes)
        self.online_min_adm.create_path_graph(self.number_of_nodes)
        self.create_paths_for_path_topology()

    def start_analysis_for_ring_topology(self):
        self.optimal_min_adm.create_cycle_graph(self.number_of_nodes)
        self.online_min_adm.create_cycle_graph(self.number_of_nodes)
        self.create_paths_for_ring_topology()

    def create_paths_for_path_topology(self):
        if self.number_of_nodes < 3:
            return
        if self.number_of_paths < 3:
            return
        number_of_paths = self.number_of_paths
        number_of_nodes = self.number_of_nodes
        i = 0
        while i < self.number_of_paths:
            if number_of_paths == 1:
                path = list(range(1, self.number_of_nodes + 1))
                self.paths.append(path)
                i += 1
                return
            number_of_paths_with_same_colour = self.getRandomNumber(self.number_of_nodes, number_of_paths)
            temp = number_of_paths_with_same_colour
            nodes_left = self.number_of_nodes
            k = 1
            while k < self.number_of_nodes and temp > 0:
                max_step = nodes_left - temp
                if (temp == 1) or (max_step == 1):
                    step = max_step
                else:
                    if max_step < 1:
                        continue
                    else:
                        step = rnd.randint(1, max_step)
                path = list(range(k, k + step + 1))
                self.paths.append(path)
                k += step
                nodes_left -= step
                temp -= 1
            number_of_paths -= number_of_paths_with_same_colour
            i += number_of_paths_with_same_colour

    def getRandomNumber(self, number_of_nodes, number_of_paths):
        if number_of_paths == 2:
            number_of_paths_with_same_colour = 2
        else:
            if number_of_paths < number_of_nodes:
                number_of_paths_with_same_colour = rnd.randint(2, number_of_paths)
            else:
                number_of_paths_with_same_colour = rnd.randint(2, self.number_of_nodes - 1)
        return number_of_paths_with_same_colour

    def create_paths_for_ring_topology(self):
        if self.number_of_nodes < 3:
            return
        if self.number_of_paths < 3:
            return
        number_of_paths = self.number_of_paths
        number_of_nodes = self.number_of_nodes
        i = 0
        while i < self.number_of_paths:
            if number_of_paths == 1:
                path = list(range(1, self.number_of_nodes+1))
                path.append(1)
                # path = list(range(1, rnd.randint(2, self.number_of_nodes)))
                self.paths.append(path)
                i += 1
                return
            number_of_paths_with_same_colour = self.getRandomNumberForCycleGraph(self.number_of_nodes, number_of_paths)
            temp = number_of_paths_with_same_colour
            nodes_left = self.number_of_nodes + 1
            k = 1
            while k < self.number_of_nodes + 1 and temp > 0:
                max_step = nodes_left - temp
                if (temp == 1) or (max_step == 1):
                    step = max_step
                else:
                    step = rnd.randint(1, max_step)
                if temp == 1:
                    if k == self.number_of_nodes:
                        path = [k, 1]
                    else:
                        path = list(range(k, k + step))
                        path.append(1)
                else:
                    path = list(range(k, k + step + 1))
                self.paths.append(path)
                k += step
                nodes_left -= step
                temp -= 1
            number_of_paths -= number_of_paths_with_same_colour
            i += number_of_paths_with_same_colour

    def getRandomNumberForCycleGraph(self, number_of_nodes, number_of_paths):
        if number_of_paths == 2:
            number_of_paths_with_same_colour = 2
        else:
            if number_of_paths < number_of_nodes:
                number_of_paths_with_same_colour = rnd.randint(2, number_of_paths)
            else:
                number_of_paths_with_same_colour = rnd.randint(2, self.number_of_nodes)
        return number_of_paths_with_same_colour

    def calculate_optimal_sol(self):
        self.optimal_min_adm.all_colours = list(range(1, 1001))
        for path in self.paths:
            self.optimal_min_adm.add_light_path(path)
        self.optimal_sol = sum(self.optimal_min_adm.adm)

    def calculate_random_sol(self):
        self.online_min_adm.clear_algorithm_without_graph()
        self.online_min_adm.all_colours = list(range(1, 1001))
        self.online_sol = 0
        my_list = list(self.paths)
        rnd.shuffle(my_list)
        for path in my_list:
            self.online_min_adm.add_light_path(path)
        self.online_sol = sum(self.online_min_adm.adm)


if __name__ == "__main__":
    test_path_topology = min_adm_analysis()
    test_path_topology.__init__()
    test_path_topology.start_analysis(40, 80, 'p')
    print(f"competitive ratio is {test_path_topology.competitive_ratio}")
    test_ring_topology = min_adm_analysis()
    test_ring_topology.__init__()
    test_ring_topology.start_analysis(10, 20, 'r')
    print(f"the optimal sol is {test_ring_topology.optimal_sol}")
    print(f"the online sol is {test_ring_topology.online_sol}")
    print(f"competitive ratio is {test_ring_topology.competitive_ratio}")
