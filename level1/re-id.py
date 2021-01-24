def eratosthenes(integers):
    # recursive implementation of the eratosthenes algorithm
    if integers[0] ** 2 > integers[-1]:
        return integers
    else:
        return [integers[0]] + eratosthenes(
            [integer for integer in integers if integer % integers[0] != 0]
        )


def solution(i):
    prime_numbers = eratosthenes(range(2, 100000))
    concatenated_prime_numbers_string = "".join(
        [str(prime_number) for prime_number in prime_numbers]
    )
    assert len(concatenated_prime_numbers_string) > 10000
    return concatenated_prime_numbers_string[i : i + 5]
