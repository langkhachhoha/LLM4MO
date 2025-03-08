from codebleu import calc_codebleu

prediction = "import numpy as np\n\ndef select_next_node(current_node, destination_node, unvisited_nodes, distance_matrix_1, distance_matrix_2):\n    min_sum = np.inf\n    next_node = None\n    \n    for node in unvisited_nodes:\n        node_sum = distance_matrix_1[current_node][node] + distance_matrix_2[current_node][node]\n        if node_sum < min_sum:\n            min_sum = node_sum\n            next_node = node\n            \n    return next_node"


reference = "import numpy as np\n\ndef select_next_node(current_node, destination_node, unvisited_nodes, distance_matrix_1, distance_matrix_2):\n    min_sum_distance = np.inf\n    next_node = None\n    \n    for node in unvisited_nodes:\n        dist_sum = distance_matrix_1[current_node][node] + distance_matrix_2[current_node][node]\n        if dist_sum < min_sum_distance:\n            min_sum_distance = dist_sum\n            next_node = node\n    \n    return next_node"

result = calc_codebleu([reference], [prediction], lang="python", weights=(0.25, 0.25, 0.25, 0.25), tokenizer=None)['codebleu']
print(result)

