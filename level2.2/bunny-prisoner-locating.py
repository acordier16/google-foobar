def solution(x, y):
    # moving from (1, 1) to (1, 2) is +1
    # moving from (1, 2) to (2, 3) is +2, etc.
    moving_up = sum(range(1, y))
    # once we moved up the first column, we move to the right
    moving_right = sum(range(y + 1, y + x))
    return str(1 + moving_up + moving_right)
