import sys
import re
import itertools

node_regex = re.compile(r'''/dev/grid/node-
                            x(\d+)-y(\d+)
                            \s+(\d+)T        # size
                            \s+(\d+)T        # used
                            \s+(\d+)T        # avail
                            \s+(\d+)%        # use%''',
                        re.VERBOSE)

class Node:
    pass

def parse(line):
    m = re.match(node_regex, line)
    node = Node()
    (x, y, size, used, avail, _) = tuple(map(int, m.groups()))
    node.pos = (x, y)
    node.size = size
    node.used = used
    node.avail = avail
    # ignore use%
    return node

def part1(nodes):
    sizes = sorted(nodes, key=lambda node: node.used)
    avails = sorted(nodes, key=lambda node: node.avail)
    compatible = 0
    i = 0
    for src in sizes:
        if src.used == 0:
            continue
        while i < len(avails) and avails[i].avail < src.used:
            i = i + 1
        compatible = compatible + len(avails) - i
        if src.avail >= src.used:
            compatible = compatible - 1

    return compatible

def part1_brute_force(nodes):
    return sum(len([dst for dst in nodes
                    if src.used != 0 and dst.avail >= src.used and src.pos != dst.pos])
               for src in nodes)


if __name__ == '__main__':
    nodes = [parse(line.rstrip())
             for line in itertools.islice(sys.stdin, 2, None)] # drop 2
    print part1_brute_force(nodes)
    print part1(nodes)
