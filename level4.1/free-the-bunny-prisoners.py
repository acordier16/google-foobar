import itertools


def solution(n_bunnies, n_required):
    # We know that n_required - 1 bunnies should not be able to open the door with the keys,
    # which gives us the number of keys
    n_keys = len(list(itertools.combinations(range(n_bunnies), n_required - 1)))
    # For each key, we will distribute (n_buns - n_required + 1) copies of the key to the bunnies
    n_bunnies_per_key = n_bunnies - n_required + 1

    # In order to respect the lexicographic order, we will distribute each key in the following order:
    # (in case n_bunnies = 5, and n_bunnies_per_key = 3)
    # key 0 is given to bunnies 0, 1, and 2
    # key 1 is given to bunnnies 0, 1, and 3
    # key 2 is given to bunnies 0, 1, and 4
    # key 3 is given to bunnies 0, 2, 3
    # etc.
    solution = [[] for i in range(n_bunnies)]
    for i, bunny_indexes in enumerate(
        itertools.combinations(range(n_bunnies), n_bunnies_per_key)
    ):
        # Distribute the i key to the concerned bunnies
        # (len(bunny_indexes) is equal to n_bunnies_per_key)
        for bunny_index in bunny_indexes:
            solution[bunny_index].append(i)

    return solution
