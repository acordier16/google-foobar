def solution(i):
    """
    Fastest way to go down to 1 is as follows:
    Divide by 2 if the number is even.
    Add or substract 1 if the number is odd.
    To know if you should rather add or substract 1 for odd numbers, we can
    write the number in base 2: it ends either with 01 or 10 (because it is odd).
    If it ends with 01, we should substract 1 (so that we get 00 at the end,
    and it gives a better multiple of 2). If it ends with 10, we should add 1
    (so that we get 00 at the end as well).
    Note: there is an exception for 3 = 11, for which we should rather remove 1.
    """
    number_of_operations = 0
    i = int(i)
    while i != 1:
        if i % 2 == 0:
            i = i / 2
        else:
            if (i - 1) % 4 == 0 or i == 3:
                i = i - 1
            elif (i + 1) % 4 == 0:
                i = i + 1
        number_of_operations += 1
    return str(number_of_operations)
