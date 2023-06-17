import os


class Files_management:
    def __init__(self, paths, number_of_nodes, number_of_paths, ring_or_path, optimal_sol):
        self.paths = paths
        self.optimal_sol = optimal_sol
        self.number_of_nodes = number_of_nodes
        self.number_of_paths = number_of_paths
        self.ring_or_path = ring_or_path
        self.file_directory = f"networks_paths_data/{ring_or_path}_topology/"

    def store_data_in_file(self):
        # os.makedirs(self.file_directory, exist_ok=True)
        file_name = f"network_{self.number_of_nodes}_{self.number_of_paths}.txt"
        file_path = f"{self.file_directory}{file_name}"
        with open(file_path, 'w') as file:
            text = f"{self.ring_or_path} topology\n" \
                   f"number of nodes={self.number_of_nodes}\n" \
                   f"number of paths={self.number_of_paths}\n" \
                   f"optimal solution={self.optimal_sol}\n" \
                   f"the optimal order:\n"
            file.write(text)
            for path in self.paths:
                line = f"{path}\n"
                file.write(line)



