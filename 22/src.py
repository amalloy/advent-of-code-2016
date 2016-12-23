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
    node.x = x
    node.y = y
    node.size = size
    node.used = used
    node.avail = avail
    # ignore use%
    return node

if __name__ == '__main__':
    nodes = [parse(line.rstrip())
             for line in itertools.islice(sys.stdin, 2, None)] # drop 2
    for node in nodes:
        print vars(node)
