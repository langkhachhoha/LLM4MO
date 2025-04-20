class GetPrompts():
    def __init__(self):
        self.prompt_task = "You are solving a Bi-objective Travelling Salesman Problem (bi-TSP), where each node has two different 2D coordinates: \
(x1, y1) and (x2, y2), representing its position in two objective spaces. The goal is to find a tour visiting each node exactly once and returning \
to the starting node, while minimizing two objectives simultaneously: the total tour length in each coordinate space. \
Given an archive of non-dominated solutions, where each solution is a numpy array representing a TSP tour, and its corresponding objective \
is a tuple of two values (cost in each space), design a heuristic function named 'select_neighbor' that selects one solution from the archive \
and generates a neighbor solution from it. Do not choose randomly. Instead, think about how to identify a solution that is promising for further  \
local improvement. Using a novel or creative strategy — not necessarily 2-opt. You can try swap, reinsertion, segment relocation, or invent your own local \
transformation logic.  The function should return the new neighbor solution."

        self.prompt_func_name = "select_neighbor"
        self.prompt_func_inputs = ["archive", "instance", "distance_matrix_1", "distance_matrix_2"]
        self.prompt_func_outputs = ["new_solution"]

        self.prompt_inout_inf = "'archive' is a list of (solution, objective) pairs. \
Each 'solution' is a numpy array of node IDs. Each 'objective' is a tuple of two float values. \
'distance_matrix_1' and 'distance_matrix_2' are numpy arrays representing pairwise distances between nodes. \
'instance' is a numpy array of shape (N, 4), where each row corresponds to a node and contains its coordinates in two 2D spaces: (x1, y1, x2, y2)."

        self.prompt_other_inf = "All inputs are Numpy-compatible."




    def get_task(self):
        return self.prompt_task
    
    def get_func_name(self):
        return self.prompt_func_name
    
    def get_func_inputs(self):
        return self.prompt_func_inputs
    
    def get_func_outputs(self):
        return self.prompt_func_outputs
    
    def get_inout_inf(self):
        return self.prompt_inout_inf

    def get_other_inf(self):
        return self.prompt_other_inf

if __name__ == "__main__":
    getprompts = GetPrompts()
    print(getprompts.get_task())
