import sys
import itertools

def next(row):
    prev = '.' + row + '.'
    return "".join('.' if prev[i] == prev[i+2] else '^' for i in xrange(len(row)))

def iterate(f, x):
    while True:
        yield x
        x = f(x)

if __name__ == '__main__':
    start = sys.stdin.next().rstrip()
    rows = iterate(next, start)
    print sum(s.count('.') for s in itertools.islice(rows, 40))
