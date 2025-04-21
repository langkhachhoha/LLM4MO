import random
import matplotlib.pyplot as plt

# ==== Step 1: Sinh dữ liệu mock ====
def generate_mock_data(n=100):
    population = []
    for _ in range(n):
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        population.append({'objective': [x, y]})
    return population

# ==== Step 2: Pareto sorting ====
def is_dominated(obj1, obj2):
    return all(o1 <= o2 for o1, o2 in zip(obj1, obj2)) and any(o1 < o2 for o1, o2 in zip(obj1, obj2))

def fast_non_dominated_sort(population):
    fronts = []
    S = {}
    n = {}
    rank = {}

    for i, p in enumerate(population):
        S[i] = []
        n[i] = 0
        for j, q in enumerate(population):
            if i == j:
                continue
            if is_dominated(p['objective'], q['objective']):
                S[i].append(j)
            elif is_dominated(q['objective'], p['objective']):
                n[i] += 1
        if n[i] == 0:
            rank[i] = 0
            if len(fronts) == 0:
                fronts.append([])
            fronts[0].append(i)

    i = 0
    while i < len(fronts):
        next_front = []
        for p_idx in fronts[i]:
            for q_idx in S[p_idx]:
                n[q_idx] -= 1
                if n[q_idx] == 0:
                    rank[q_idx] = i + 1
                    next_front.append(q_idx)
        if next_front:
            fronts.append(next_front)
        i += 1
    return fronts

# ==== Step 3: Crowding Distance ====
def calculate_crowding_distance(population, indices):
    distances = {i: 0.0 for i in indices}
    num_objectives = len(population[0]['objective'])

    for m in range(num_objectives):
        indices.sort(key=lambda i: population[i]['objective'][m])
        distances[indices[0]] = distances[indices[-1]] = float('inf')
        min_obj = population[indices[0]]['objective'][m]
        max_obj = population[indices[-1]]['objective'][m]
        if max_obj == min_obj:
            continue
        for k in range(1, len(indices) - 1):
            prev_obj = population[indices[k - 1]]['objective'][m]
            next_obj = population[indices[k + 1]]['objective'][m]
            distances[indices[k]] += (next_obj - prev_obj) / (max_obj - min_obj)
    return distances

# ==== Step 4: Chọn đúng N cá thể ====
def population_management(population, N):
    fronts = fast_non_dominated_sort(population)
    selected = []

    for front in fronts:
        if len(selected) + len(front) <= N:
            selected.extend(front)
        else:
            remaining = N - len(selected)
            distances = calculate_crowding_distance(population, front)
            sorted_front = sorted(front, key=lambda i: -distances[i])
            selected.extend(sorted_front[:remaining])
            break
    return selected

# ==== Step 5: Vẽ biên Pareto ====
def plot_selected(population, selected_indices):
    all_x = [ind['objective'][0] for ind in population]
    all_y = [ind['objective'][1] for ind in population]

    sel_x = [population[i]['objective'][0] for i in selected_indices]
    sel_y = [population[i]['objective'][1] for i in selected_indices]

    plt.figure(figsize=(8, 6))
    plt.scatter(all_x, all_y, label='All Individuals', alpha=0.3)
    plt.scatter(sel_x, sel_y, color='red', label='Selected (N)', marker='x')
    plt.title('Selected N Individuals via Pareto Front + Diversity')
    plt.xlabel('Objective 1')
    plt.ylabel('Objective 2')
    plt.legend()
    plt.grid(True)
    plt.show()

# ==== Step 6: Chạy toàn bộ ====
if __name__ == "__main__":
    population = generate_mock_data(100)
    N = 30
    selected_indices = population_management(population, N)
    print(population)
    plot_selected(population, selected_indices)

