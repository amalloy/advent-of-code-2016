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

def prune(times, (prime, residue)):
    return itertools.ifilter(lambda t: t % prime == residue, times)

def solve(constraints):
    constraints = sorted(constraints, reverse=True)
    times = reduce(prune, constraints, itertools.count())
    return times.next()

if __name__ == '__main__':
    constraints = [parse(line.rstrip()) for line in sys.stdin]
    print "part 1: %d" % solve(constraints)

    print "part 2: %d" % solve(constraints +
            [parse("Disc #7 has 11 positions; at time=0, it is at position 0.")])
