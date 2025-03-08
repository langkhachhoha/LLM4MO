import heapq
import numpy as np

def dominates(ind1, ind2):
    """Kiểm tra nếu ind1 Pareto dominates ind2."""
    return all(x <= y for x, y in zip(ind1, ind2)) and any(x < y for x, y in zip(ind1, ind2))

def pareto_filter(pop):
    """Lọc Pareto Front từ quần thể."""
    pareto_front = []
    for individual in pop:
        dominated = False
        for other in pop:
            if dominates(other['objective'], individual['objective']):
                dominated = True
                break
        if not dominated:
            pareto_front.append(individual)
    return pareto_front

def crowding_distance_sort(pop):
    """Sắp xếp theo Crowding Distance để đảm bảo sự đa dạng."""
    num_objectives = len(pop[0]['objective']) if pop else 0
    distances = {id(ind): 0 for ind in pop}  # Sử dụng id để tránh lỗi key

    for i in range(num_objectives):
        pop.sort(key=lambda x: x['objective'][i])  # Sắp xếp theo từng mục tiêu
        min_val = pop[0]['objective'][i]
        max_val = pop[-1]['objective'][i]

        if max_val == min_val:
            continue  # Nếu mọi giá trị giống nhau, bỏ qua

        distances[id(pop[0])] = float('inf')  # Gán vô cực cho biên
        distances[id(pop[-1])] = float('inf')

        for j in range(1, len(pop) - 1):
            prev_obj = pop[j - 1]['objective'][i]
            next_obj = pop[j + 1]['objective'][i]
            distances[id(pop[j])] += (next_obj - prev_obj) / (max_val - min_val)

    return sorted(pop, key=lambda x: distances[id(x)], reverse=True)  # Sắp xếp giảm dần theo crowding distance

def population_management(pop, size):
    """Quản lý quần thể để đảm bảo đầu ra có đúng `size` phần tử."""
    pop = [ind for ind in pop if ind['objective'] is not None]  # Lọc cá thể không hợp lệ

    if size > len(pop):
        size = len(pop)  # Nếu quần thể quá nhỏ, chỉ lấy tối đa có thể

    # Loại bỏ trùng lặp
    unique_pop = []
    unique_objectives = set()
    for individual in pop:
        obj_tuple = tuple(individual['objective'])
        if obj_tuple not in unique_objectives:
            unique_pop.append(individual)
            unique_objectives.add(obj_tuple)

    # Lọc Pareto Front
    pareto_front = pareto_filter(unique_pop)

    # Nếu Pareto Front nhiều hơn `size`, chọn bằng crowding distance
    if len(pareto_front) > size:
        return crowding_distance_sort(pareto_front)[:size]

    # Nếu Pareto Front nhỏ hơn `size`, bổ sung cá thể khác từ quần thể
    remaining = size - len(pareto_front)
    non_pareto = [ind for ind in unique_pop if ind not in pareto_front]

    if remaining > 0 and non_pareto:
        additional_individuals = heapq.nsmallest(remaining, non_pareto, key=lambda x: sum(x['objective']))
        pareto_front += additional_individuals

    return pareto_front











