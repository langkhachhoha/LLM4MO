import math
import os
from os import path
import numpy as np
import sys
import argparse
from scipy.spatial import distance_matrix
import logging
from copy import copy
try:
    from gpt import select_next_node_v2 as select_next_node
except:
    from gpt import select_next_node

def eval_heuristic(node_positions_1: np.ndarray, node_positions_2: np.ndarray) -> tuple[float, float]:
    '''
    Generate solution for 2-objective TSP problem using the GPT-generated heuristic algorithm.
    
    Parameters
    ----------
    node_positions_1 : np.ndarray
        2D array of node positions in space 1 of shape (problem_size, 2).
    node_positions_2 : np.ndarray
        2D array of node positions in space 2 of shape (problem_size, 2).
    
    Returns
    -------
    obj1, obj2 : tuple[float, float]
        The length of the generated tour in space 1 and space 2 respectively.
    '''
    problem_size = node_positions_1.shape[0]

    dist_mat1 = distance_matrix(node_positions_1, node_positions_1)
    dist_mat2 = distance_matrix(node_positions_2, node_positions_2)
    

    start_node = 0
    solution = [start_node]

    unvisited = set(range(problem_size))
    unvisited.remove(start_node)
    

    for _ in range(problem_size - 1):
        next_node = select_next_node(
            current_node=solution[-1],
            destination_node=start_node,
            unvisited_nodes=copy(unvisited),
            distance_matrix_1=dist_mat1.copy(),
            distance_matrix_2=dist_mat2.copy()
        )
        solution.append(next_node)
        if next_node in unvisited:
            unvisited.remove(next_node)
        else:
            raise KeyError(f"Node {next_node} is already visited.")
    
    obj1 = 0
    obj2 = 0
    for i in range(problem_size):
        next_i = (i + 1) % problem_size
        obj1 += dist_mat1[solution[i], solution[next_i]]
        obj2 += dist_mat2[solution[i], solution[next_i]]
    
    return obj1, obj2

if __name__ == '__main__':
    print("[*] Running ...")

    problem_size = int(sys.argv[1])
    root_dir = sys.argv[2]
    mood = sys.argv[3]
    assert mood in ['train', 'val']

    basepath = os.path.join(os.path.dirname(__file__), "dataset")

    if not os.path.isfile(os.path.join(basepath, "train50_dataset.npz")):
        from gen_inst import generate_datasets
        generate_datasets()
    
    if mood == 'train':
        dataset_path = os.path.join(basepath, f"train{problem_size}_dataset.npz")
        data = np.load(dataset_path)

        node_positions_1 = data['space1']
        node_positions_2 = data['space2']
        n_instances = node_positions_1.shape[0]
        print(f"[*] Dataset loaded: {dataset_path} with {n_instances} instances.")
        
        objs1 = []
        objs2 = []
        for i in range(n_instances):
            obj1, obj2 = eval_heuristic(node_positions_1[i], node_positions_2[i])
            print(f"[*] Instance {i}: obj1 = {obj1}, obj2 = {obj2}")
            objs1.append(obj1)
            objs2.append(obj2)
        
        print("[*] Average:")
        print("Objective 1:", np.mean(objs1))
        print("Objective 2:", np.mean(objs2))
    
    else:
        for problem_size in [20, 50, 100, 200]:
            dataset_path = os.path.join(basepath, f"val{problem_size}_dataset.npz")
            logging.info(f"[*] Evaluating {dataset_path}")
            data = np.load(dataset_path)
            node_positions_1 = data['space1']
            node_positions_2 = data['space2']
            n_instances = node_positions_1.shape[0]
            objs1 = []
            objs2 = []
            for i in range(n_instances):
                obj1, obj2 = eval_heuristic(node_positions_1[i], node_positions_2[i])
                objs1.append(obj1)
                objs2.append(obj2)
            print(f"[*] Average for {problem_size}:")
            print("Objective 1:", np.mean(objs1))
            print("Objective 2:", np.mean(objs2))
