import numpy as np
import random
from codebleu import calc_codebleu

def ast_similarity(code1, code2):
    return calc_codebleu([code1], [code2], "python")['syntax_match_score']


def dominates(ind1, ind2):
    return all(x <= y for x, y in zip(ind1, ind2)) and any(x < y for x, y in zip(ind1, ind2))


def compute_dissimilarity(pop):
    N = len(pop)
    S = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i != j:
                S[i, j] = -ast_similarity(pop[i]['code'], pop[j]['code']) 
    return S

def compute_dominance_mask(pop):
    N = len(pop)
    D = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i != j and dominates(pop[i]['objective'], pop[j]['objective']):
                D[i, j] = 1
    return D

def population_management(pop, size):
    """Quản lý quần thể để đảm bảo đầu ra có đúng `size` phần tử."""
    N = len(pop)
    if N == 0:
        return []
    pop = [ind for ind in pop if ind['objective'] is not None]  # Lọc cá thể không hợp lệ
    S = compute_dissimilarity(pop)
    D = compute_dominance_mask(pop)
    S_prime = S * D
    v = np.sum(S_prime, axis=0)
    k = np.argsort(-v)
    
    new_population = [pop[i] for i in k[:size]]
    return new_population

if __name__ == "__main__":
    # Mock population with objective values
    mock_population = [
        {"id": 1, "code": "def f(): return 1", "objective": [3, 5]},
        {"id": 2, "code": "def f(): return 2", "objective": [4, 3]},
        {"id": 3, "code": "def f(): return 3", "objective": [2, 6]},
        {"id": 4, "code": "def f(): return 4", "objective": [7, 2]},
        {"id": 5, "code": "def f(): return 5", "objective": [5, 4]},
        {"id": 6, "code": "def f(): return 6", "objective": [6, 1]},
        {"id": 7, "code": "def f(): return 7", "objective": [1, 7]},
    ]

    # Mock population size
    mock_size = 4  # Desired output size

    # Run population management
    filtered_population = population_management(mock_population, mock_size)

    # Print result
    print("Filtered Population:")
    for individual in filtered_population:
        print(f"ID: {individual['id']}, Objective: {individual['objective']}")


