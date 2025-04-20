# Mở file results/pops/population_generation_10.json và vẽ biên pareto theo objective 
import json
with open("results/pops/population_generation_10.json", "r") as f:
    data = json.load(f)

import matplotlib.pyplot as plt
import numpy as np
# Extract the objectives from the data
objectives = np.array([ind['objective'] for ind in data])
print(objectives)

# Draw the Pareto front regarding the objectives
plt.figure(figsize=(10, 6))
plt.scatter(objectives[:, 0], objectives[:, 1], color='blue', label='Pareto Front', marker='*')
plt.xlabel("Negative Hypervolume")
plt.ylabel("Time")
plt.title("Pareto Front - Bi-objective TSP via SEMO - MEoH")
plt.grid(True)
plt.legend()
plt.show()

