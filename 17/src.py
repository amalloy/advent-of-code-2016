import sys
import Queue
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

def search(root):
    q = Queue.PriorityQueue()
    q.put((0 + root.goal_estimate(), 0, root))
    iterations = 0
    while not q.empty():
        (estimated_cost, spent_cost, node) = q.get()
        iterations = iterations + 1
        if iterations % 1 == 5000:
            print "Moved %d so far, about %d from goal" % (spent_cost, estimated_cost)
        for (spend, next) in node.nexts():
            kind = next.evaluate()
            if kind == 'fail':
                continue
            new_cost = spent_cost + spend
            if kind == 'succeed':
                return (new_cost, next)
            q.put_nowait((new_cost + next.goal_estimate(), new_cost, next))

if __name__ == '__main__':
    pass
