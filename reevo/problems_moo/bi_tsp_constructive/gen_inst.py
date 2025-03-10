import numpy as np
import os

def generate_datasets():
    basepath = os.path.join(os.path.dirname(__file__), "dataset")
    os.makedirs(basepath, exist_ok=True)

    np.random.seed(1234)

    for problem_size in [50]:
        n_instances = 64
        dataset_space1 = np.random.rand(n_instances, problem_size, 2)
        dataset_space2 = np.random.rand(n_instances, problem_size, 2)
        np.savez(os.path.join(basepath, f'train{problem_size}_dataset.npz'),
                 space1=dataset_space1, space2=dataset_space2)

    for problem_size in [20, 50, 100, 200]:
        n_instances = 64
        dataset_space1 = np.random.rand(n_instances, problem_size, 2)
        dataset_space2 = np.random.rand(n_instances, problem_size, 2)
        np.savez(os.path.join(basepath, f'val{problem_size}_dataset.npz'),
                 space1=dataset_space1, space2=dataset_space2)
        
    for problem_size in [20, 50, 100, 200, 500, 1000]:
        n_instances = 64
        dataset_space1 = np.random.rand(n_instances, problem_size, 2)
        dataset_space2 = np.random.rand(n_instances, problem_size, 2)
        np.savez(os.path.join(basepath, f'test{problem_size}_dataset.npz'),
                 space1=dataset_space1, space2=dataset_space2)

if __name__ == "__main__":
    generate_datasets()
