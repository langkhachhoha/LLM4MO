import numpy as np
import random
from copy import deepcopy



def cal_knee_point(pop):
    knee_point = np.zeros(len(pop[0]['objective']))
    m = len(pop[0]['objective'])
    for i in range(m):
        knee_point[i] = 1e9
    for indi in pop:
        for i in range(m):
            knee_point[i] = min(knee_point[i], indi['objective'][i])
    return knee_point


def cal_nadir_point(pop):
    m = len(pop[0]['objective'])
    nadir_point = np.zeros(m)
    for i in range(m):
        nadir_point[i] = -1e9
    for indi in pop:
        for i in range(m):
            nadir_point[i] = max(nadir_point[i], indi['objective'][i])
    return nadir_point



def Generation_PFG(pop, GK, knee_point, nadir_point, sigma):
    m = len(knee_point)
    d = [(nadir_point[j] - knee_point[j] + 2 * sigma) / GK for j in range(m)]

    # Tính Grid cho từng cá thể
    Grid = []
    for indi in pop:
        grid_indi = [(indi['objective'][j] - knee_point[j] + sigma) // d[j] for j in range(m)]
        Grid.append(grid_indi)

    # Khởi tạo PFG: m mục tiêu, mỗi mục tiêu có GK đoạn
    PFG = [[[] for _ in range(GK)] for _ in range(m)]

    for i in range(m):  # với từng mục tiêu
        for j in range(GK):  # với từng đoạn
            # Tìm S_i(j): các cá thể thuộc đoạn thứ j của mục tiêu thứ i
            Sij = [idx for idx, g in enumerate(Grid) if g[i] == j]

            if not Sij:
                continue

            # Tìm giá trị nhỏ nhất theo Grid của các cá thể này (theo toàn bộ vector grid)
            g_min = min(Grid[idx][i] for idx in Sij)

            # Chọn những cá thể trong đoạn j có grid = g_min cho mục tiêu i
            for idx in Sij:
                if Grid[idx][i] == g_min:
                    PFG[i][j].append(pop[idx])

    return PFG


import random
def parent_selection(pop, m, GK = 4, sigma = 0.01, crossover_rate = 0.9):
    knee_point = cal_knee_point(pop)
    nadir_point = cal_nadir_point(pop)
    PFG = Generation_PFG(pop, GK, knee_point, nadir_point, sigma)
    if (random.random() > crossover_rate):
        parents = random.choices(pop, k=m)
    else:
        i = random.randint(0, len(knee_point)) 
        j = random.randint(0, len(PFG[i]) - 1)
        while len(PFG[i][j]) == 0:
            i = random.randint(0, len(knee_point)) 
            j = random.randint(0, len(PFG[i]) - 1)

        parents = random.choices(PFG[i][j] + PFG[i][j + 1], k=m)

    return parents, PFG

# ==== Step 1: Sinh dữ liệu mock ====
def generate_mock_data(n=100):
    population = []
    for _ in range(n):
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        population.append({'objective': [x, y]})
    return population


import matplotlib.pyplot as plt

def plot_pfg(pop, GK, knee_point, nadir_point, sigma):
    # Vẽ toàn bộ điểm trong quần thể
    x_vals = [indi['objective'][0] for indi in pop]
    y_vals = [indi['objective'][1] for indi in pop]

    # Tính khoảng cách mỗi lưới theo mục tiêu
    d = [(nadir_point[j] - knee_point[j] + 2 * sigma) / GK for j in range(len(knee_point))]

    # Thiết lập lưới theo 2 mục tiêu
    x_grids = [knee_point[0] - sigma + i * d[0] for i in range(GK + 1)]
    y_grids = [knee_point[1] - sigma + i * d[1] for i in range(GK + 1)]

    # Vẽ scatter các cá thể
    plt.figure(figsize=(8, 6))
    plt.scatter(x_vals, y_vals, color='blue', label='Individuals')

    # Vẽ lưới theo trục x (mục tiêu 0)
    for x in x_grids:
        plt.axvline(x, color='gray', linestyle='--', linewidth=0.8)

    # Vẽ lưới theo trục y (mục tiêu 1)
    for y in y_grids:
        plt.axhline(y, color='gray', linestyle='--', linewidth=0.8)

    # Đánh dấu knee và nadir
    plt.scatter([knee_point[0]], [knee_point[1]], color='green', marker='x', s=100, label='Knee Point')
    plt.scatter([nadir_point[0]], [nadir_point[1]], color='red', marker='*', s=100, label='Nadir Point')

    plt.xlabel("Objective 1")
    plt.ylabel("Objective 2")
    plt.title("PFG Grid Visualization")
    plt.legend()
    plt.grid(True)
    plt.show()






if __name__ == "__main__":
    pop = generate_mock_data(100)
    m = 4
    parents, PFG = parent_selection(pop, m)
    cnt = 0
    # Dem so phan tu trong PFG
    for i in range(len(PFG)):
        for j in range(len(PFG[i])):
            cnt += len(PFG[i][j])
    print("Total elements in PFG:", cnt)