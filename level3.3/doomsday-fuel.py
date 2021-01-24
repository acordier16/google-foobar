from fractions import Fraction, gcd
import math

# Matrix operations functions inspired from
# https://stackoverflow.com/questions/32114054/matrix-inversion-without-numpy
def transpose_matrix(matrix):
    return map(list, zip(*matrix))


def get_matrix_minor(matrix, i, j):
    return [row[:j] + row[j + 1 :] for row in (matrix[:i] + matrix[i + 1 :])]


def get_matrix_determinant(matrix):
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    determinant = 0
    for c in range(len(matrix)):
        determinant += (
            ((-1) ** c)
            * matrix[0][c]
            * get_matrix_determinant(get_matrix_minor(matrix, 0, c))
        )
    return determinant


def get_matrix_inverse(matrix):
    determinant = get_matrix_determinant(matrix)
    if len(matrix) == 2:
        return [
            [matrix[1][1] / determinant, -1 * matrix[0][1] / determinant],
            [-1 * matrix[1][0] / determinant, matrix[0][0] / determinant],
        ]
    cofactors = []
    for r in range(len(matrix)):
        cofactor_row = []
        for c in range(len(matrix)):
            minor = get_matrix_minor(matrix, r, c)
            cofactor_row.append(((-1) ** (r + c)) * get_matrix_determinant(minor))
        cofactors.append(cofactor_row)
    cofactors = transpose_matrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c] / determinant
    return cofactors


# End of matrix operations functions from stackoverflow


def swap_matrix_lines(matrix, a, b):
    matrix[a], matrix[b] = matrix[b], matrix[a]
    return matrix


def swap_matrix_columns(matrix, a, b):
    for row in matrix:
        row[a], row[b] = row[b], row[a]
    return matrix


def lcm(a, b):
    """
    Least common denominator (for putting fractions
    to the same denominator at the end of the solution)
    """
    return abs(a * b) // gcd(a, b)


def lcm_on_a_list(l):
    """
    Returns, for a given list of integers, their least
    common denominator.
    """
    if len(l) == 2:
        return lcm(l[0], l[1])
    return lcm_on_a_list([lcm(l[0], l[1])] + l[2:])


def solution(matrix):
    """
    matrix is a squre matrix of form (for example)
    [
      [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
      [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
      [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
      [0,0,0,0,0,0],  # s3 is terminal
      [0,0,0,0,0,0],  # s4 is terminal
      [0,0,0,0,0,0],  # s5 is terminal
    ]
    This lecture on absorbing Markov chains was of great help:
    https://math.dartmouth.edu/archive/m20x06/public_html/Lecture14.pdf
    It would be better to cut this big function into multiple small ones for algebra
    operations on matrices (though that's the purpose of the numpy library).
    """
    # The input matrix is almost a transition matrix for a Markov chain.
    # We first need to sort it (while keeping the order of the terminal states)
    # so that the first states are non-terminal, while the states at the end
    # are terminal
    for n in range(len(matrix)):
        for x in range(len(matrix) - 1):
            first_row = matrix[x]
            second_row = matrix[x + 1]
            if sum(first_row) == 0 and sum(second_row) != 0:
                matrix = swap_matrix_lines(matrix, x, x + 1)
                matrix = swap_matrix_columns(matrix, x, x + 1)

    # We first replace the 0 in the terminal states with a 1 where needed in
    # order to get a proper Markov chain.
    # Example: for s3, [0, 0, 0, 0, 0, 0] becomes [0, 0, 0, 1, 0, 0]
    # (s3 is terminal, so it loops on its own state indefinitely)
    nb_non_terminal_states = 0
    for i, row in enumerate(matrix):
        # edge case, where the starting state is a terminal state
        if i == 0 and sum(row) == 0:
            return [1, 1]

        if sum(row) == 0:
            for j, element in enumerate(row):
                if i == j:
                    matrix[i][j] = 1
        else:
            nb_non_terminal_states += 1

    # We then transform the numbers into probabilities (fractions)
    for i, row in enumerate(matrix):
        row_sum = sum(row)
        for j, element in enumerate(row):
            matrix[i][j] = Fraction(matrix[i][j], row_sum)

    # We separate the transition matrix between non-terminal and terminal states
    # e.g. (s0, s1) vs (s2, s3, s4, ...) in our example (since we sorted
    # non-terminal from terminal states first)
    q = [
        row[:nb_non_terminal_states] for row in matrix[:nb_non_terminal_states]
    ]  # top-left (s0, s1)x(s0,s1) sub-matrix in the transition matrix
    r = [
        row[nb_non_terminal_states:] for row in matrix[:nb_non_terminal_states]
    ]  # top-right (s0, s1)x(s2,s3,s4,s5) sub-matrix in the transition matrix

    # Let's now compute the fundamental matrix: q:= (identity - q)(^-1)
    # We do q:= (identity - q)
    for i, row in enumerate(q):
        for j, element in enumerate(row):
            if i == j:
                q[i][j] = 1 - q[i][j]
            else:
                q[i][j] = -q[i][j]
    # We do q := invert(q)
    q = get_matrix_inverse(q)

    # We do q * r (matrix multiplication)
    # Output will be a 2x(nb_terminal_states) shape matrix
    # where every element in position i,j is the probability to end
    # in the terminal state j, starting from the state i
    probabilities_matrix = []
    for i in range(len(q)):
        probabilities_matrix.append([])
        for j in range(len(r[0])):
            row_vector = q[i]
            column_vector = [r[x][j] for x in range(len(r))]
            scalar_product = sum(
                [row_vector[x] * column_vector[x] for x in range(len(row_vector))]
            )
            probabilities_matrix[-1].append(scalar_product)

    # s0 will always be the starting state, hence we only need the first row
    # (we also need to take the absolute value in order to get something positive
    probabilities = [abs(proba) for proba in probabilities_matrix[0]]
    lcm_denominator = lcm_on_a_list([proba.denominator for proba in probabilities])
    answer = [int((proba * lcm_denominator).numerator) for proba in probabilities] + [
        lcm_denominator
    ]
    return answer
