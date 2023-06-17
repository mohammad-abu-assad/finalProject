from MINADM_analysis import min_adm_analysis
from files_management import Files_management


class Experiments_for_the_algorithm:
    def __init__(self, ax, canvas, path_or_ring):
        self.ax = ax
        self.canvas = canvas
        self.path_or_ring = path_or_ring

    def start_experiments(self):
        analysis = min_adm_analysis()

        for number_of_nodes in range(10, 101, 10):
            f = number_of_nodes // 2
            t = number_of_nodes * 2
            for number_of_paths in range(f, t + 1, 5):
                analysis.__init__()
                analysis.start_analysis(number_of_nodes, number_of_paths, self.path_or_ring[0])
                competitive_ratio = analysis.competitive_ratio
                file_management = Files_management(analysis.paths, number_of_nodes, number_of_paths
                                                   , self.path_or_ring, analysis.optimal_sol)
                file_management.store_data_in_file()
                line = f"{number_of_nodes},{number_of_paths},{competitive_ratio}\n"
                file_name = f"{self.path_or_ring}_topology_analysis_data.txt"
                with open(file_name, 'a') as file:
                    file.write(line)
                x = number_of_nodes
                y = number_of_paths
                z = competitive_ratio
                self.ax.scatter(x, y, z, s=50, c='red')
                self.canvas.draw()
