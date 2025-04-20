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

def parent_selection(pop, m):
    """
    Implements the ParentSelection algorithm.

    Parameters:
    - pop: List of individuals, where each individual is a dictionary with:
        - 'code': Source code string.
        - 'objective': List of objective values.
    - m: Number of parents to select.

    Returns:
    - A list of selected parents.
    """
    if not pop:
        return []
    pop = [ind for ind in pop if ind['objective'] is not None]  # Lọc cá thể không hợp lệ

    N = len(pop)
    S = compute_dissimilarity(pop)
    D = compute_dominance_mask(pop)

    # Compute selection probabilities
    S_prime = S * D
    v = np.sum(S_prime, axis=0)
    pi = np.exp(v) / np.sum(np.exp(v))  # Softmax normalization

    # Sample parents based on probabilities
    parents = random.choices(pop, weights=pi, k=m)
    return parents


if __name__ == "__main__":
    # --- Mock Data Generation ---
    def generate_mock_population(size):
        """
        Generate a mock population.
        Each individual has:
        - 'code': A simple Python function as a string.
        - 'objective': A list of random objective values.
        """
        code_snippets = [
            "def add(a, b): return a + b",
            "def subtract(a, b): return a - b",
            "def multiply(a, b): return a * b",
            "def divide(a, b): return a / b if b != 0 else None",
            "def power(a, b): return a ** b",
            "def sqrt(x): return x ** 0.5",
            "def factorial(n): return 1 if n == 0 else n * factorial(n-1)",
            "def gcd(a, b): return a if b == 0 else gcd(b, a % b)",
            "def lcm(a, b): return abs(a*b) // gcd(a, b)",
            "def mod(a, b): return a % b"
        ]
        
        pop = []
        for i in range(size):
            pop.append({
                'code': code_snippets[i % len(code_snippets)],
                'objective': [random.randint(1, 10) for _ in range(3)]
            })
        
        return pop

    # Example usage
    mock_population = generate_mock_population(10)
    selected_parents = parent_selection(mock_population, 5)

    print("Mock Population:")
    for ind in mock_population:
        print(ind)

    print("\nSelected Parents:")
    for parent in selected_parents:
        print(parent)
