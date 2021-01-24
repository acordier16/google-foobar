MAXIMUM_FLOW = 2000000  # or float("Inf")


def transform_matrix_into_single_source_and_sink(entrances, exits, matrix):
    # We put the source in the 0 position
    source_row = [0 for i in range(len(matrix))]
    for i in range(len(source_row)):
        if i in entrances:
            source_row[i] = MAXIMUM_FLOW
    matrix = [source_row] + matrix

    for i in range(len(matrix)):
        matrix[i] = [0] + matrix[i]

    # We now put the sink in the -1 position
    exits = [
        exit + 1 for exit in exits
    ]  # we have to shift the exits because we added the single source
    for i in range(len(matrix)):
        if i in exits:
            matrix[i].append(MAXIMUM_FLOW)
        else:
            matrix[i].append(0)
    matrix.append([0 for i in range(len(matrix[0]))])
    return matrix


def find_path(matrix):
    """
    Breadth-first search algorithm for exploring a graph
    and finding a path
    """
    # this will be a path in the "parent" sense
    # i.e. a path that is to be read in the reverse order
    # e.g. if path = [-1, 0, 1, 1, 2, 4]
    # then the path is sink -> 4 -> 2 -> 1 -> 0 (= source)
    path = [None for i in range(len(matrix))]

    # We parse all connected nodes
    visited_nodes = []
    nodes_to_visit = [0]  # starting from the source (0)
    while True:
        # We explore nodes from the first node to visit
        # Greedy version: we explore nodes only if they would allow at least the maximum bunnies possible
        maximum_value = 0
        for node_indice, value in enumerate(matrix[nodes_to_visit[0]]):
            # If node connected to this node and not visited yet (we don't want to cycle) and not in "to visit"
            if (
                value > maximum_value
                and node_indice not in visited_nodes
                and node_indice not in nodes_to_visit
            ):
                # We append the found node to "to visit" status
                maximum_value = value
                nodes_to_visit.append(node_indice)
                path[node_indice] = nodes_to_visit[0]

        # We consider the current node as visited
        visited_nodes.append(nodes_to_visit[0])
        nodes_to_visit.pop(0)

        # If no more nodes to explore, we return None (no path found)
        if len(nodes_to_visit) == 0:
            return None

        # If we reached the sink, we end the path search and return the path (we found a path!)
        if nodes_to_visit[0] == len(matrix) - 1:
            return path


def solution(entrances, exits, matrix):
    """
    Edmonds-Karp algorithm for computing maximum flow.
    This (french) lecture on maximum flow was useful:
    - https://moodle.utc.fr/file.php/141/Transparents_du_cours/Flot_maximum_RO03-2011.pdf
    As well as wikipedia for maximum flow, Ford-Fulkerson and Edmons-Karp algorithms.
    - https://fr.wikipedia.org/wiki/Probl%C3%A8me_de_flot_maximum
    - https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm
    """
    # Let's  first  transform the network (matrix) into
    # a single source and single sink network
    matrix = transform_matrix_into_single_source_and_sink(entrances, exits, matrix)

    maximum_flow = 0
    path = find_path(matrix)

    while path != None:  # while we can find a path
        # compute the flow
        current_node = (
            -1
        )  # we will move along the path up from the sink (end of graph) to the source (beginning of graph)
        current_path_flow = MAXIMUM_FLOW
        while current_node != 0:  # while not at source
            current_path_flow = min(
                current_path_flow, matrix[path[current_node]][current_node]
            )
            current_node = path[current_node]  # move towards source
        maximum_flow += current_path_flow

        # adjust (update) the residual graph
        # (from sink to source)
        v = -1
        while v != 0:
            u = path[v]
            matrix[u][v] -= current_path_flow
            matrix[v][u] += current_path_flow
            v = path[v]

        # find an new path
        path = find_path(matrix)

    return maximum_flow
