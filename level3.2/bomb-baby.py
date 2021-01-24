def recursive_solution(x, y, counter):
    """
    A recursive solution that goes up the tree towards the origin (1,1) by
    dividing the two numbers with each other. Another less efficient solution
    is to substract the two numbers with each other to count the whole path one
    step by one step.
    """
    x = int(x)
    y = int(y)

    # if one of the two terms is 1, solution is trivial:
    # the path length is the other term minus one
    if x == 1:
        return str(counter + (y - 1))
    if y == 1:
        return str(counter + (x - 1))

    biggest = max(x, y)
    smallest = min(x, y)
    if biggest % smallest == 0:
        return "impossible"
    else:
        counter += biggest // smallest
        return recursive_solution(smallest, biggest % smallest, counter)


def solution(x, y):
    return recursive_solution(x, y, 0)
