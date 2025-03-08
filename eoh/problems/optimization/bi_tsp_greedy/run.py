import numpy as np
import pickle
import sys
import types
import warnings
from .prompts import GetPrompts
from .get_instance import GetData

class BITSPCONST():
    def __init__(self) -> None:
        self.ndelay = 1
        self.problem_size = 50
        self.neighbor_size = np.minimum(self.problem_size,self.problem_size)
        self.n_instance = 8  
        self.running_time = 10



        self.prompts = GetPrompts()

        getData = GetData(self.n_instance,self.problem_size)
        self.instance_data = getData.generate_instances()
        

    def tour_cost(self, instance, solution, problem_size):

            # cost_1, cost_2 = self.tour_cost(instance,route,self.problem_size)
        # print(instance)
        cost_1 = 0
        cost_2 = 0
        
        for j in range(problem_size - 1):
            node1, node2 = int(solution[j]), int(solution[j + 1])
            
            coord_1_node1, coord_2_node1 = instance[node1][:2], instance[node1][2:]
            coord_1_node2, coord_2_node2 = instance[node2][:2], instance[node2][2:]

            cost_1 += np.linalg.norm(coord_1_node1 - coord_1_node2)
            cost_2 += np.linalg.norm(coord_2_node1 - coord_2_node2)
        
        node_first, node_last = int(solution[0]), int(solution[-1])
        
        coord_1_first, coord_2_first = instance[node_first][:2], instance[node_first][2:]
        coord_1_last, coord_2_last = instance[node_last][:2], instance[node_last][2:]

        cost_1 += np.linalg.norm(coord_1_last - coord_1_first)
        cost_2 += np.linalg.norm(coord_2_last - coord_2_first)

        return cost_1, cost_2  

    def generate_neighborhood_matrix(self,instance):
        instance = np.array(instance)
        n = len(instance)
        neighborhood_matrix = np.zeros((n, n), dtype=int)

        for i in range(n):
            distances = np.linalg.norm(instance[i] - instance, axis=1)
            sorted_indices = np.argsort(distances)  # sort indices based on distances
            neighborhood_matrix[i] = sorted_indices

        return neighborhood_matrix 


    #@func_set_timeout(5)
    def greedy(self,eva):

        dis_1 = np.ones(self.n_instance)
        dis_2 = np.ones(self.n_instance)
        n_ins = 0
        for instance, distance_matrix_1, distance_matrix_2 in self.instance_data:
            neighbor_matrix = self.generate_neighborhood_matrix(instance)


            destination_node = 0

            current_node = 0

            route = np.zeros(self.problem_size)
            for i in range(1,self.problem_size-1):

                near_nodes = neighbor_matrix[current_node][1:]

                mask = ~np.isin(near_nodes,route[:i])

                unvisited_near_nodes = near_nodes[mask]

                unvisited_near_size = np.minimum(self.neighbor_size,unvisited_near_nodes.size)

                unvisited_near_nodes = unvisited_near_nodes[:unvisited_near_size]

                next_node = eva.select_next_node(current_node, destination_node, unvisited_near_nodes, distance_matrix_1, distance_matrix_2)

                if next_node in route:
                    print("wrong algorithm select duplicate node, retrying ...")
                    return None

                current_node = next_node

                route[i] = current_node

                #print(">>> Step "+str(i)+": select node "+str(instance[current_node][0])+", "+str(instance[current_node][1]))
            # print(route)

            mask = ~np.isin(np.arange(self.problem_size),route[:self.problem_size-1])

            last_node = np.arange(self.problem_size)[mask]

            current_node = last_node[0]

            route[self.problem_size-1] = current_node

            #print(">>> Step "+str(self.problem_size-1)+": select node "+str(instance[current_node][0])+", "+str(instance[current_node][1]))
            cost_1, cost_2 = self.tour_cost(instance,route,self.problem_size)

            dis_1[n_ins] = cost_1
            dis_2[n_ins] = cost_2

            n_ins += 1
            if n_ins == self.n_instance:
                break
            #self.route_plot(instance,route,self.oracle[n_ins])


        ave_dis_1 = np.average(dis_1)
        ave_dis_2 = np.average(dis_2)
        #print("average dis: ",ave_dis)

        return ave_dis_1, ave_dis_2


    def evaluate(self, code_string):
        # print("Evaluating heuristic...")
        try:
            # Suppress warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                # Create a new module object
                heuristic_module = types.ModuleType("heuristic_module")
                
                # Execute the code string in the new module's namespace
                exec(code_string, heuristic_module.__dict__)

                # Add the module to sys.modules so it can be imported
                sys.modules[heuristic_module.__name__] = heuristic_module

                # Now you can use the module as you would any other
                fitness = self.greedy(heuristic_module)
                return fitness
        except Exception as e:
            return None
            


