def partial_order(a, b):
    """
    This function defines a partial order over the versions, recursively
    (from major to revision).
    It will return True if a > b (a "newer than" b), and False if b > a
    (b "newer than" a). If the two versions are exactly equal (a = b),
    it will return False (convention only, this shouldn't happen anyway
    in the context of this exercise).
    """

    # If we "run out of numbers" for a version, that means
    # this version is the earliest
    if len(a) == 0:
        return False
    elif len(b) == 0:
        return True

    a_split = [int(element) for element in a.split(".")]
    b_split = [int(element) for element in b.split(".")]

    if a_split[0] > b_split[0]:
        return True
    elif a_split[0] < b_split[0]:
        return False
    else:
        return partial_order(
            ".".join([str(element) for element in a_split[1:]]),
            ".".join([str(element) for element in b_split[1:]]),
        )


def solution(l):
    """
    This will sort the list of versions according to a partial order defined above.
    This sort is a recursive selective sort and thus sub-optimal both memory-wise and
    time-wise.
    A better solution could be to sort according to the first rule (major version),
    then the second rule (minor), and then the third (revision).
    """

    if len(l) == 1:
        return l

    max_version = l[0]
    max_version_index = 0
    for version_index, version in enumerate(l):
        if partial_order(version, max_version):
            max_version = version
            max_version_index = version_index
    l.remove(max_version)
    return solution(l) + [max_version]
