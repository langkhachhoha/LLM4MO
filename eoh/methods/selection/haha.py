# import random
# import numpy as np
# import matplotlib.pyplot as plt


# num_cities = 20
# coords_1 = np.random.rand(num_cities, 2)  # Không gian 1
# coords_2 = np.random.rand(num_cities, 2)  # Không gian 2

# def random_solution():
#     sol = list(range(num_cities))
#     random.shuffle(sol)
#     return sol


# def select_neighbor(archive, instance, distance_matrix_1, distance_matrix_2, ref_point, ideal_point):
#     def calculate_objective(solution, distance_matrix):
#         obj1 = np.sum([distance_matrix[solution[i], solution[(i+1) % len(solution)]] for i in range(len(solution))])
#         obj2 = np.sum([distance_matrix[solution[i], solution[(i+1) % len(solution)]] for i in range(len(solution))])
#         return obj1, obj2

#     def is_dominated(obj, other_obj):
#         return all(x <= y for x, y in zip(obj, other_obj)) and any(x < y for x, y in zip(obj, other_obj))

#     def local_search(solution, distance_matrix_1, distance_matrix_2):
#         improved = True
#         while improved:
#             improved = False
#             for i in range(len(solution)):
#                 for j in range(i + 2, len(solution)):
#                     new_solution = solution.copy()
#                     new_solution[i:j] = np.flip(new_solution[i:j])
#                     new_obj1, new_obj2 = calculate_objective(new_solution, distance_matrix_1), calculate_objective(new_solution, distance_matrix_2)
#                     if (not is_dominated(new_obj1, obj1) or not is_dominated(new_obj2, obj2)) and not (new_obj1 == obj1 and new_obj2 == obj2):
#                         solution = new_solution
#                         obj1, obj2 = new_obj1, new_obj2
#                         improved = True
#                         break
#                 if improved:
#                     break
#         return solution

#     selected_solution, (obj1, obj2) = np.random.choice(archive)
#     new_solution = local_search(selected_solution, distance_matrix_1, distance_matrix_2)
#     return new_solution


# import numpy as np
# import pickle
# import sys
# import types
# import warnings
# import random
# import time 


        

# def tour_cost(instance, solution, problem_size):
#         cost_1 = 0
#         cost_2 = 0
        
#         for j in range(problem_size - 1):
#             node1, node2 = int(solution[j]), int(solution[j + 1])
            
#             coord_1_node1, coord_2_node1 = instance[node1][:2], instance[node1][2:]
#             coord_1_node2, coord_2_node2 = instance[node2][:2], instance[node2][2:]

#             cost_1 += np.linalg.norm(coord_1_node1 - coord_1_node2)
#             cost_2 += np.linalg.norm(coord_2_node1 - coord_2_node2)
        
#         node_first, node_last = int(solution[0]), int(solution[-1])
        
#         coord_1_first, coord_2_first = instance[node_first][:2], instance[node_first][2:]
#         coord_1_last, coord_2_last = instance[node_last][:2], instance[node_last][2:]

#         cost_1 += np.linalg.norm(coord_1_last - coord_1_first)
#         cost_2 += np.linalg.norm(coord_2_last - coord_2_first)

#         return cost_1, cost_2  
    

# def dominates(self, a, b):
#         """True if a dominates b (minimization)."""
#         return all(x <= y for x, y in zip(a, b)) and any(x < y for x, y in zip(a, b))

# def random_solution(self):
#         sol = list(range(20))
#         random.shuffle(sol)
#         return np.array(sol)



# def semo(self,eva):
#         obj_1 = np.ones(self.n_instance)
#         obj_2 = np.ones(self.n_instance)
#         n_ins = 0
#         for instance, distance_matrix_1, distance_matrix_2 in self.instance_data:
#             start = time.time()
#             s = [self.random_solution() for _ in range(10)]
#             Archive = [(s_, self.tour_cost(instance, s_, self.problem_size)) for s_ in s]
#             for _ in range(2000):
#                 s_prime = eva.select_neighbor(Archive, instance, distance_matrix_1, distance_matrix_2, self.ref_point, self.ideal_point)
#                 f_s_prime = self.tour_cost(instance, s_prime, self.problem_size)

#                 # Nếu không bị thống trị
#                 if not any(self.dominates(f_a, f_s_prime) for _, f_a in Archive):
#                     # Loại bỏ các phần tử bị thống trị bởi f_s_prime
#                     Archive = [(a, f_a) for a, f_a in Archive if not self.dominates(f_s_prime, f_a)]
#                     # Thêm nghiệm mới
#                     Archive.append((s_prime, f_s_prime))
#             end = time.time()
#             objs = np.array([obj for _, obj in Archive])
#             # Tính HV
#             hv_indicator = HV(ref_point=self.ref_point)
#             hv_value = hv_indicator(objs)
#             obj_1[n_ins] = -hv_value
#             obj_2[n_ins] = end - start
#             n_ins += 1
#         # Trả về các giá trị mục tiêu
#         return np.mean(obj_1), np.mean(obj_2)
            


#     def evaluate(self, code_string):
#         # print("Evaluating heuristic...")
#         try:
#             # Suppress warnings
#             with warnings.catch_warnings():
#                 warnings.simplefilter("ignore")
#                 # Create a new module object
#                 heuristic_module = types.ModuleType("heuristic_module")
                
#                 # Execute the code string in the new module's namespace
#                 exec(code_string, heuristic_module.__dict__)

#                 # Add the module to sys.modules so it can be imported
#                 sys.modules[heuristic_module.__name__] = heuristic_module

#                 # Now you can use the module as you would any other
#                 fitness = self.semo(heuristic_module)
#                 return fitness
#         except Exception as e:
#             return None


# def semo_biobjective_tsp(max_iter=5000):
#     s = [random_solution() for _ in range(10)]
#     A = [(s_, evaluate(s_)) for s_ in s]

#     for _ in range(max_iter):
#         s, f_s = random.choice(A)
#         s_prime = get_neighbor(s)
#         f_s_prime = evaluate(s_prime)

#         # Nếu không bị thống trị
#         if not any(dominates(f_a, f_s_prime) for _, f_a in A):
#             # Loại bỏ các phần tử bị thống trị bởi f_s_prime
#             A = [(a, f_a) for a, f_a in A if not dominates(f_s_prime, f_a)]
#             # Thêm nghiệm mới
#             A.append((s_prime, f_s_prime))

#     return A

# # -------------------------------
# # CHẠY THUẬT TOÁN & VẼ BIÊN PARETO
# # -------------------------------

# pareto_front = semo_biobjective_tsp()


# objs = np.array([obj for _, obj in pareto_front])
# plt.figure(figsize=(8, 6))
# plt.scatter(objs[:, 0], objs[:, 1], c='blue', label='Pareto Front')
# plt.xlabel("Tour length in space 1")
# plt.ylabel("Tour length in space 2")
# plt.title("Pareto Front - Bi-objective TSP via SEMO")
# plt.grid(True)
# plt.legend()
# plt.show()


# from pymoo.indicators.hv import HV

# # Reference point
# ref_point = np.array([20.0, 20.0])

# # Tính HV
# hv_indicator = HV(ref_point=ref_point)
# hv_value = hv_indicator(objs)
# print(f"Hypervolume: {hv_value}") 




print("""Hello {'algorithm': '\nThe algorithm selects a random solution from the archive, applies a 2-opt move to generate a neighbor solution by swapping two edges in the tour, and returns the new neighbor solution.\n', 'code': 'import numpy as np\nimport random\n\ndef select_neighbor(archive, instance, distance_matrix_1, distance_matrix_2):\n    selected_solution, _ = random.choice(archive)\n    \n    def calculate_tour_length(solution, distance_matrix):\n        return sum(distance_matrix[solution[i], solution[i + 1]] for i in range(len(solution) - 1)) + distance_matrix[solution[-1], solution[0]]\n    \n    def two_opt(solution):\n        new_solution = solution.copy()\n        i, j = random.sample(range(len(solution)), 2)\n        if i > j:\n            i, j = j, i\n        new_solution[i:j+1] = new_solution[i:j+1][::-1]\n        return new_solution\n    \n    new_solution = two_opt(selected_solution)\n    \n    return new_solution', 'objective': None, 'other_inf': None}""")