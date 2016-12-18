import sys
import Queue
import itertools
from md5 import md5

puzzle_input = 'pvhmgsws'
dirs = {'D': (1, 0), 'U': (-1, 0), 'L': (0, -1), 'R': (0, 1)}

def hash(s):
  return md5(puzzle_input + s).hexdigest()

def doors(path):
    s = hash(path)
    for i, d in enumerate('UDLR'):
        if s[i] in 'bcdef':
            yield (d, dirs[d])

class Node:
    def __init__(self, coords, path):
        self.coords = coords
        self.path = path

    def evaluate(self):
        if self.coords == (3, 3):
            return 'succeed'
        if any(x < 0 or x > 3 for x in self.coords):
            return 'fail'
        return 'progress'

    def goal_estimate(self):
        return 6 - self.coords[0] - self.coords[1]

    def nexts(self):
        (y, x) = self.coords
        return [(1, Node((y + dy, x + dx), self.path + dir))
                for (dir, (dy, dx)) in doors(self.path)]

def paths(root):
    q = [(0, root)]
    while q:
        (spent_cost, node) = q.pop()
        for (spend, next) in node.nexts():
            kind = next.evaluate()
            if kind == 'fail':
                continue
            new_cost = spent_cost + spend
            if kind == 'succeed':
                yield (new_cost, next)
            else:
                q.append((new_cost, next))

if __name__ == '__main__':
    solutions = itertools.imap(lambda x: x[1].path, paths(Node((0,0), '')))
    low = solutions.next()
    hi = low
    for soln in solutions:
        low = min([low, soln], key=len)
        hi = max([hi, soln], key=len)
    print "part1: %s, part2: %s" % (low, hi)
