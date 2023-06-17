import networkx as nx


class online_min_adm_algorithm:
    def __init__(self):
        self.graph = nx.Graph()
        self.adm = []
        self.paths = []
        self.conflict_graph = nx.Graph()
        self.share_graph = nx.Graph()
        self.path_colour = []
        self.colour_paths = dict()
        self.colours = []
        self.all_colours = [
            'red', 'blue', 'green', 'orange', 'purple', 'pink', 'cyan', 'magenta',
            'yellow', 'teal', 'lime', 'maroon', 'navy', 'olive', 'silver', 'aqua',
            'fuchsia', 'indigo', 'gold', 'orchid', 'brown', 'crimson', 'gray', 'black'
        ]
        self.colour_number = 0

    def clear_algorithm(self):
        self.graph.clear()
        self.adm.clear()
        self.paths.clear()
        self.colour_paths.clear()
        self.conflict_graph.clear()
        self.share_graph.clear()
        self.path_colour.clear()
        self.colour_number = 0

    def clear_algorithm_without_graph(self):
        for i in range(len(self.adm)):
            self.adm[i] = 0
        self.paths.clear()
        self.colour_paths.clear()
        self.conflict_graph.clear()
        self.share_graph.clear()
        self.path_colour.clear()
        self.colour_number = 0

    def create_path_graph(self, number_of_nodes):
        self.graph = nx.path_graph(number_of_nodes)
        if number_of_nodes == 0:
            return
        self.graph = nx.relabel_nodes(self.graph, {i: i + 1 for i in range(number_of_nodes)})
        for i in range(number_of_nodes + 1):
            self.adm.append(0)

    def create_cycle_graph(self, number_of_nodes):
        self.graph = nx.cycle_graph(number_of_nodes)
        if number_of_nodes == 0:
            return
        self.graph = nx.relabel_nodes(self.graph, {i: i + 1 for i in range(number_of_nodes)})

        for i in range(number_of_nodes + 1):
            self.adm.append(0)

    def add_light_path(self, path):
        self.paths.append(path)
        self.add_path_to_conflict_graph()
        self.add_path_to_share_graph()
        self.assign_colour()

    def add_path_to_conflict_graph(self):
        path_number = len(self.paths) - 1
        path_to_add = self.paths[path_number]
        self.conflict_graph.add_node(path_number)
        if self.conflict_graph.number_of_nodes() == 1:
            return
        starting = path_to_add[0]
        ending = path_to_add[-1]
        if starting == ending:
            for path in range(path_number):
                self.conflict_graph.add_edge(path_number, path)
            return

        temp = list(path_to_add)
        temp.reverse()
        for path in range(path_number):
            intersection = set(path_to_add).intersection(set(self.paths[path]))
            if self.paths[path] == path_to_add:
                self.conflict_graph.add_edge(path_number, path)
                continue
            if self.paths[path] == temp:
                self.conflict_graph.add_edge(path_number, path)
                continue
            if len({starting, ending}.intersection({self.paths[path][0], self.paths[path][-1]})) == 2:
                pass
            elif len(intersection) >= 2:
                self.conflict_graph.add_edge(path_number, path)

    def add_path_to_share_graph(self):
        path_number = len(self.paths) - 1
        path_to_add = self.paths[path_number]
        self.share_graph.add_node(path_number)
        if self.share_graph.number_of_nodes() == 1:
            return
        conflicts = list(self.conflict_graph.edges())

        for path in range(path_number):
            if (path_number, path) in conflicts or (path, path_number) in conflicts:
                pass
            else:
                intersection = set(path_to_add).intersection(set(self.paths[path]))
                if len(intersection) == 0:
                    pass
                else:
                    self.share_graph.add_edge(path_number, path, label=intersection)

    def assign_colour(self):
        path_number = len(self.paths) - 1
        path_to_add = self.paths[path_number]
        starting = path_to_add[0]
        ending = path_to_add[-1]
        if len(self.paths) == 1:
            self.colours.append(self.all_colours[0])
            self.colour_paths.update({self.colours[0]: list([path_number])})
            self.path_colour.append(self.colours[0])
            self.adm[starting] += 1
            self.adm[ending] += 1
            self.colour_number += 1
            return True
        if starting == ending:
            if self.colour_number == len(self.all_colours):
                return False
            self.colours.append(self.all_colours[self.colour_number])
            self.colour_paths.update({self.colours[-1]: [path_number]})
            self.path_colour.append(self.colours[-1])
            self.adm[starting] += 1
            self.colour_number += 1
            return

        for i in range(self.colour_number):
            colour = self.colours[i]
            flag = 0
            paths_with_same_colour = self.colour_paths[colour]
            conflicts = list(self.conflict_graph.edges())
            for p in paths_with_same_colour:
                if (path_number, p) in conflicts or (p, path_number) in conflicts:
                    flag = 1
                    break
            if flag == 1:
                continue
            path = self.union_all(paths_with_same_colour)

            if len({starting, ending}.intersection({path[0], path[-1]})) == 2:
                self.path_colour.append(colour)
                self.colour_paths[colour].append(path_number)
                return True

        for i in range(self.colour_number):
            colour = self.colours[i]
            flag = 0
            paths_with_same_colour = self.colour_paths[colour]
            conflicts = list(self.conflict_graph.edges())
            for p in paths_with_same_colour:
                if (path_number, p) in conflicts or (p, path_number) in conflicts:
                    flag = 1
                    break
            if flag == 1:
                continue
            path = self.union_all(paths_with_same_colour)
            intersection = list({starting, ending}.intersection({path[0], path[-1]}))
            if len(intersection) == 1:
                index = {starting, ending}
                index.discard(intersection[0])
                index = list(index)
                self.adm[index[0]] += 1
                self.path_colour.append(colour)
                self.colour_paths[colour].append(path_number)
                return True

        if self.colour_number == len(self.all_colours):
            return False

        self.colours.append(self.all_colours[self.colour_number])
        self.colour_paths.update({self.colours[-1]: [path_number]})
        self.path_colour.append(self.colours[-1])
        self.adm[starting] += 1
        self.adm[ending] += 1
        self.colour_number += 1
        return True

    def union_all(self, to_union):

        union_all_paths = list()
        if len(to_union) == 1:
            return list(self.paths[to_union[0]])

        for path in to_union:
            union_all_paths = self.merge_two_lists(union_all_paths, list(self.paths[path]))

        return list(union_all_paths)

    def merge_two_lists(self, first_list, second_list):
        if not first_list:
            return second_list
        first_list_start = first_list[0]
        first_list_end = first_list[-1]
        second_list_start = second_list[0]
        second_list_end = second_list[-1]
        merge = list()
        if first_list_end == second_list_start:
            second_list.pop(0)
            merge = first_list + second_list

        elif second_list_end == first_list_start:
            first_list.pop(0)
            merge = second_list + first_list

        elif second_list_start == first_list_start:
            second_list.pop(0)
            second_list.reverse()
            merge = second_list + first_list

        elif second_list_end == first_list_end:
            first_list.pop(-1)
            first_list.reverse()
            merge = second_list + first_list

        return merge

    def solution(self):
        sol = []
        for colour in self.colours:
            sol.append(tuple(self.colour_paths[colour]))

        return sol


if __name__ == "__main__":
    test_ring_topology = online_min_adm_algorithm()
    test_ring_topology.create_cycle_graph(5)
    print("\n\nring topology test: ")
    print("the input is cycle graph with 5 node (1 - 5)")
    paths = [[1, 2, 3], [3, 4], [4, 5], [5, 1], [1, 2, 3, 4, 5], [5, 1], [1, 2], [2, 3], [3, 4, 5], [5, 1]]
    for i in range(len(paths)):
        print(f"path {i} arrived: {paths[i]}")
        test_ring_topology.add_light_path(paths[i])
        print(f"path colour = {test_ring_topology.path_colour[i]}")
        print(f"ADM after adding the path: {test_ring_topology.adm}")
        print(test_ring_topology.paths)
    print(f"the solution is : {test_ring_topology.solution()}")
    print(f"total ADMs= {sum(test_ring_topology.adm)} ADMs")
