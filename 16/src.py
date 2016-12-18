import sys
import itertools

puzzle_input = '01111001100111011'

def iterate(f, x):
    while True:
        yield x
        x = f(x)

def expand(s):
    return s + "0" + "".join('1' if c == '0' else '0' for c in s[::-1])

def pairs(s):
    return zip(*[iter(s)] * 2)

def checksum(s):
    return "".join('1' if x == y else '0' for x, y in pairs(s))

def first_not(pred, xs):
    return itertools.dropwhile(pred, xs).next()

def checksum_filled_disk(size):
    expansions = iterate(expand, puzzle_input)
    data = first_not(lambda s: len(s) < size, expansions)[:size]
    return first_not(lambda s: len(s) % 2 == 0, iterate(checksum, data))

if __name__ == '__main__':
    print checksum_filled_disk(272)
    print checksum_filled_disk(35651584)
