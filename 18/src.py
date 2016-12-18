import sys
import itertools

def next(row):
    prev = '.' + row + '.'
    return "".join('.' if prev[i] == prev[i+2] else '^' for i in xrange(len(row)))

def iterate(f, x):
    while True:
        yield x
        x = f(x)

def solve(init, num_rows):
    return sum(s.count('.') for s in itertools.islice(iterate(next, init), num_rows))

if __name__ == '__main__':
    start = sys.stdin.next().rstrip()
    print "part1: %d" % solve(start, 40)
    print "part2: %d" % solve(start, 400000)
