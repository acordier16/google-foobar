from itertools import product
from collections import defaultdict

"""
    The process the nebula goes through is similar to the "game of life",
    because of the "locality" of the process.
    These kind of processes are more broadly called "cellular automatons".
    The goal of this exercise is to find the number of inputs that will lead to
    a given output, following the described nebula automaton.
    Because the process uses "stride 1" and not "stride 2", there is no
    independency between each 2x2 window, and the "overlaps" have to be
    taken into account for computing the result, since they condition the
    number of possibilities.

    Thinking process for the solution:
    - First and foremost, I tried brute-forcing with every (n+1, m+1) possibility.
    It works, but obviously very slow and doesn't scale (O(2^((n+1)*(m+1))))
    - Then, realized I could build the solutions iteratively "row by row". This
    would be equivalent to brute-forcing row-by-row, or to build a tree of solutions
    in the row space and pruning dead ends. It would speed-up the baseline brute-force method,
    but only when we have a lot of rows.
    - I therefore decided to explore an extension of this solution where I would build "row by row"
    and "column by column" at the same time, but it implied storing the built solution matrices.
    Because of this, I did not manage to make it work as fast as the "row-only" approach easily.
    - At this point I realized that I could simply transpose the matrix (doesn't change the result)
    for high-number-of-columns regimes, and went for the "row by row" solution.

    Thinking process for optimizing this code:
    - First i had to optimize the computation of the "double-rows -> row process", going from
    multiple for-loops and if's to a simple look-up with list comprehension.
    - Then I needed to replace the data structure I was using for the working_rows cache
    (list) with something more appropriate (defaultdict used as counters),
    sacrificing the exhibition of the constructed solutions for speed.
"""

# Generating all possible combinations
# e.g. {(False, False, True, False): True,
#       (False, False, True, True): False,
#       ...}
combination = {
    tuple_: (sum(tuple_) == 1) for tuple_ in product([True, False], repeat=4)
}


def solution(nebula):
    """
    This will build all working solutions "row by row". We first start by enumerating
    all (2, m+1) "double-rows" possibilities which would lead to the first row of our
    (n, m) nebula. We select these that work.
    Starting from that point, we can append all possible (1, m+1) rows to all the
    working "double-rows" we built, and find the "row builds" which will lead
    to the next row of our nebula.
    It is equivalent to building a "tree of solution" in the row space, and pruning
    dead ends quickly. This method will speed-up the baseline brute-force solution
    when we will have a lot of rows to deal with (but not when we will have a
    lot of columns). For that reason, if there are more columns than rows, the matrix
    will be transposed (it is relatively easy to show that the number of solutions
    is the same anyway).
    """

    # If more columns than rows, we transpose (see readme above)
    # The number of possibilities is actually the same if you transpose the matrix
    if len(nebula) < len(nebula[0]):
        nebula = list(zip(*nebula))
        nebula = [list(row) for row in nebula]

    nebula_row_length = len(nebula[0])

    # Initialization: we generate all (1, m+1) row possibilities
    working_rows = defaultdict(int)
    for k in list(product([True, False], repeat=len(nebula[0]) + 1)):
        working_rows[k] += 1

    # We iterate over rows (loop is safer than recursion if many many rows)
    for row_counter in range(1, len(nebula) + 1):
        row_possibilities = product([True, False], repeat=len(nebula[0]) + 1)
        new_working_rows = defaultdict(int)
        for row_possibility in row_possibilities:
            for working_row, count in working_rows.items():
                row1 = working_row
                row2 = row_possibility
                is_row_working = True
                for i in range(nebula_row_length):
                    if (
                        combination[(row1[i], row1[i + 1], row2[i], row2[i + 1])]
                        != nebula[row_counter - 1][
                            i
                        ]  # Look-up with a dict is the best approach I found speed-wise
                    ):
                        is_row_working = False
                        break  # We won't bother checking the whole row if some part of it is wrong
                if is_row_working:
                    new_working_rows[row_possibility] += (
                        1 * count
                    )  # We count this row one more time, multiplied by the one-level higher
                    # (you can think of it as multiplying the possibilities doing down the
                    # possibility tree, towards the leaves)

        working_rows = new_working_rows

        # If no working possibilities at that stage, return an empty list ("garden of eden")
        if len(working_rows.keys()) == 0:
            return 0

    return sum(working_rows.values())


nebula = [[True, False, True], [False, True, False], [True, False, True]]  # 4
print(solution(nebula))

nebula = [
    [True, True, False, True, False, True, False, True, True, False],
    [True, True, False, False, False, False, True, True, True, False],
    [True, True, False, False, False, False, False, False, False, True],
    [False, True, False, False, False, False, True, True, False, False],
]  # 11567
import time

start = time.time()
print("final answer sol2", solution(nebula))
end = time.time()
print("took", end - start)

nebula = [
    [True, False, True, False, False, True, True, True],
    [True, False, True, False, False, False, True, False],
    [True, True, True, False, False, False, True, False],
    [True, False, True, False, False, False, True, False],
    [True, False, True, False, False, True, True, True],
]  # 254
start = time.time()
print("final answer sol2", solution(nebula))
end = time.time()
print("took", end - start)
