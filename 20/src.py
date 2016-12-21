import sys
import re
import itertools

def parse(line):
    m = re.match(r'(\d+)-(\d+)', line)
    return tuple(map(int, m.groups()))

def collapse(rules):
    rs = iter(rules)
    curr = rs.next()
    for rule in rs:
        if curr[1] + 1 >= rule[0]: # overlaps current rule, just combine them
            curr = (curr[0], max(curr[1], rule[1]))
        else:
            yield curr
            curr = rule
    yield curr


if __name__ == '__main__':
    rules = collapse(sorted(map(parse, sys.stdin)))
    (lo, hi) = rules.next()
    allowed = lo
    prev = hi
    if lo > 0:
        print "part1: 0"
    else:
        print "part1: %d" % (hi + 1)

    for lo, hi in rules:
        allowed = allowed + (lo - prev - 1)
        prev = hi

    print "part2: %d" % allowed
