import sys
from itertools import chain

def chunks(n, input):
    for i in range(0, len(input), n):
        yield input[i:i + n]

def transpose(xs):
    return map(list, zip(*xs))

def parse(line):
    return map(int, line.split())

if __name__ == '__main__':
    valid = 0
    lines = list(sys.stdin)
    parsed = map(parse, lines)
    chunked = chunks(3, parsed)
    flipped = map(transpose, chunked)
    for [a,b,c] in chain(*flipped):
        if (a + b > c and a+c > b and b+c > a):
            valid = valid + 1
    print valid
