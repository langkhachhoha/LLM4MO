
class GetPrompts():
    def __init__(self):
        self.prompt_task = "Given a set of nodes, where each node has two sets of 2D coordinates and two corresponding distance matrices, \
you need to find a route that visits each node exactly once and returns to the starting node while minimizing both cost metrics simultaneously. \
The task can be solved step-by-step by starting from the current node and iteratively choosing the next node. \
Help me design a novel algorithm that is different from the algorithms in literature to select the next node in each step."
        self.prompt_func_name = "select_next_node"
        self.prompt_func_inputs = ["current_node", "destination_node", "unvisited_nodes", "distance_matrix_1", "distance_matrix_2"]
        self.prompt_func_outputs = ["next_node"]
        self.prompt_inout_inf = "'current_node', 'destination_node', 'next_node', and 'unvisited_nodes' are node IDs. 'distance_matrix_1' and 'distance_matrix_2' are the two distance matrices of nodes."
        self.prompt_other_inf = "All are Numpy arrays."


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
