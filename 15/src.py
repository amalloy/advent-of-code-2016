import sys
import re
import itertools

def parse(line):
    (disc_num, size, init) = re.match(
        r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).',
        line).groups()

    prime = int(size)
    residue = prime - ((int(init) + int(disc_num)) % prime)

    return (prime, residue)

def combine((p, n), (q, m)):
    x = n
    while x % q != m:
        x = x + p
    return (p * q, x)

def solve(constraints):
    return reduce(combine, sorted(constraints, reverse=True))[1]

if __name__ == '__main__':
    constraints = [parse(line.rstrip()) for line in sys.stdin]
    print "part 1: %d" % solve(constraints)

    print "part 2: %d" % solve(constraints +
            [parse("Disc #7 has 11 positions; at time=0, it is at position 0.")])
