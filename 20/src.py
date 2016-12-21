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
    if lo > 0:
        print 0
    else:
        print hi + 1
