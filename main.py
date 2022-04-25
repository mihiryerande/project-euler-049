# Problem 49:
#     Prime Permutations
#
# Description:
#     The arithmetic sequence, 1487, 4817, 8147,
#       in which each of the terms increases by 3330,
#       is unusual in two ways:
#         (i)  each of the three terms are prime, and,
#         (ii) each of the 4-digit numbers are permutations of one another.
#
#     There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes,
#       exhibiting this property, but there is one other 4-digit increasing sequence.
#
#     What 12-digit number do you form by concatenating the three terms in this sequence?

from itertools import permutations
from math import floor, sqrt


def has_same_digits(x, y):
    """
    Returns True iff `x` and `y` are permutations of the digits of each other.

    Args:
        x (int): Natural number
        y (int): Natural number

    Returns:
        (bool): True iff `x` and `y` are permutations of the digits of each other

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(x) == int and x > 0
    assert type(y) == int and y > 0
    return sorted(str(x)) == sorted(str(y))


def main():
    """
    Returns the two arithmetic sequences, each of three 4-digit primes,
      having the following properties:
        (i)  Each of the three terms is prime
        (ii) Each of the 4-digit numbers are permutations of each other's digits

    Returns:
        (Set[Tuple[int, int, int]]):
            Two interesting arithmetic sequences of primes
    """
    # Use a sieve to find all primes < 10,000
    prime_list = []
    prime_set = set()
    for x in range(2, 10**4):
        # Check whether x is prime
        i = 0
        is_prime = True
        x_mid = floor(sqrt(x)) + 1
        while i < len(prime_list) and prime_list[i] < x_mid:
            p = prime_list[i]
            if x % p == 0:
                is_prime = False
                break
            else:
                i += 1
        if is_prime:
            prime_list.append(x)
            prime_set.add(x)
        else:
            continue

    # Look through sieve to try finding interesting triples of primes
    trips = set()
    while len(prime_set) > 0:
        p = prime_set.pop()
        if p < 10**3:
            # Only checking 4-digit primes
            continue
        else:
            # Try to find a prime having same digits
            for qt in permutations(str(p)):
                q = int(''.join(qt))
                if q in prime_set:
                    # Try to form triple in different orders, using p and q
                    p0 = min(p, q)
                    p1 = max(p, q)

                    # 3rd element is below these two (p2, p0, p1)
                    p2 = 2 * p0 - p1
                    if p2 > 999 and p2 in prime_set and has_same_digits(p, p2):
                        trip = (p2, p0, p1)
                        trips.add(trip)

                    # 3rd element is between these two (p0, p2, p1)
                    p2 = (p0 + p1) // 2
                    if p2 in prime_set and has_same_digits(p, p2):
                        trip = (p0, p2, p1)
                        trips.add(trip)

                    # 3rd element is above these two (p0, p1, p2)
                    p2 = 2*p1 - p0
                    if p2 < 10**4 and p2 in prime_set and has_same_digits(p, p2):
                        trip = (p0, p1, p2)
                        trips.add(trip)
                else:
                    continue
    return trips


if __name__ == '__main__':
    num_seqs = main()
    print('Sequence of interesting primes:')
    for seq_ind, num_seq in enumerate(num_seqs):
        print('  ({}) {}'.format(seq_ind+1, ' -> '.join(map(str, num_seq))))
        print('  Increases by {}'.format(num_seq[1]-num_seq[0]))
        print('  Concat is {}'.format(''.join(map(str, num_seq))))
