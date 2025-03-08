from codebleu import calc_codebleu

prediction = """
def select_next_node(current_node, destination_node, unvisited_nodes, distance_matrix_1, distance_matrix_2):
    min_diff = np.inf
    next_node = None
    for node in unvisited_nodes:
        diff = abs(distance_matrix_1[current_node][node] + distance_matrix_1[node][destination_node] - distance_matrix_2[current_node][node] - distance_matrix_2[node][destination_node])
        if diff < min_diff:
            min_diff = diff
            next_node = node
    return next_node """


reference = """
def select_next_node(current_node, destination_node, unvisited_nodes, distance_matrix_1, distance_matrix_2):
    probabilities = np.zeros(len(unvisited_nodes))
    
    for i, node in enumerate(unvisited_nodes):
        probabilities[i] = distance_matrix_1[current_node][node] * distance_matrix_2[current_node][node]
    
    probabilities /= np.sum(probabilities)
    
    next_node = np.random.choice(unvisited_nodes, p=probabilities)
    
    return next_node
"""

result = calc_codebleu([reference], [prediction], lang="python", weights=(0.25, 0.25, 0.25, 0.25), tokenizer=None)['codebleu']
print(result)

