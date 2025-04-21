import numpy as np
import pickle
import sys
import types
import warnings
from .prompts import GetPrompts
from .get_instance import GetData
from pymoo.indicators.hv import HV 
import random
import time 

class BITSPCONST():
    def __init__(self) -> None:
        self.ndelay = 1
        self.problem_size = 100
        self.neighbor_size = np.minimum(self.problem_size,self.problem_size)
        self.n_instance = 8   
        self.running_time = 20
        self.ref_point = np.array([65.0, 65.0])
        self.ideal_point = np.array([0.0, 0.0])
        self.prompts = GetPrompts()

        getData = GetData(self.n_instance,self.problem_size)
        self.instance_data = getData.generate_instances()
        

    def tour_cost(self, instance, solution, problem_size):

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
    

    def dominates(self, a, b):
        """True if a dominates b (minimization)."""
        return all(x <= y for x, y in zip(a, b)) and any(x < y for x, y in zip(a, b))

    def random_solution(self):
        sol = list(range(self.problem_size))
        random.shuffle(sol)
        return np.array(sol)



    def semo(self,eva):

        obj_1 = np.ones(self.n_instance)
        obj_2 = np.ones(self.n_instance)
        n_ins = 0
        for instance, distance_matrix_1, distance_matrix_2 in self.instance_data:
            start = time.time()
            s = [self.random_solution() for _ in range(10)]
            Archive = [(s_, self.tour_cost(instance, s_, self.problem_size)) for s_ in s]
            for _ in range(2000):
                s_prime = eva.select_neighbor(Archive, instance, distance_matrix_1, distance_matrix_2)
                f_s_prime = self.tour_cost(instance, s_prime, self.problem_size)

                # Nếu không bị thống trị
                if not any(self.dominates(f_a, f_s_prime) for _, f_a in Archive):
                    # Loại bỏ các phần tử bị thống trị bởi f_s_prime
                    Archive = [(a, f_a) for a, f_a in Archive if not self.dominates(f_s_prime, f_a)]
                    # Thêm nghiệm mới
                    Archive.append((s_prime, f_s_prime))
            end = time.time()
            objs = np.array([obj for _, obj in Archive])
            # Tính HV
            hv_indicator = HV(ref_point=self.ref_point)
            hv_value = hv_indicator(objs)
            obj_1[n_ins] = -hv_value
            obj_2[n_ins] = end - start
            n_ins += 1
        # Trả về các giá trị mục tiêu
        return np.mean(obj_1), np.mean(obj_2)
            


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
                fitness = self.semo(heuristic_module)
                return fitness
        except Exception as e:
            return None
            

