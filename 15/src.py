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

if __name__ == '__main__':
    constraints = sorted([parse(line.rstrip()) for line in sys.stdin], reverse=True)
    times = reduce(prune, constraints, itertools.count())
    print times.next()
