import sys
import sets
import Queue

class Node:
    def __init__(self, maze, pos, pickups):
        self.maze = maze
        self.pos = pos
        self.pickups = pickups

    def evaluate(self):
        (y, x) = self.pos
        try:
            if not self.pickups:
                return 'succeed'
            if self.maze[y][x] == '#':
                return 'fail'
            return 'progress'
        except:
            return 'fail' # out of bounds

    def nexts(self):
        (y, x) = self.pos
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if abs(dy + dx) == 1:
                    new_pos = (y + dy, x + dx)
                    if new_pos in self.pickups:
                        new_pickups = sets.ImmutableSet({pickup for pickup in self.pickups if pickup != new_pos})
                    else:
                        new_pickups = self.pickups

                    yield (1, Node(self.maze, new_pos, new_pickups))

    def goal_estimate(self):
        return min(self.dist(pickup) for pickup in self.pickups)

    def dist(self, (y, x)):
        (j, i) = self.pos
        return abs(j - y) + abs(i - x)

    def uniq_key(self):
        return (self.pos, self.pickups)

def search(root):
    q = Queue.PriorityQueue()
    visited = set([])
    q.put((0 + root.goal_estimate(), 0, root))
    while not q.empty():
        (estimated_cost, spent_cost, node) = q.get()
        for spend, next in node.nexts():
            uniq_key = next.uniq_key()
            if uniq_key in visited:
                continue
            kind = next.evaluate()
            if kind == 'fail':
                continue
            new_cost = spent_cost + spend
            if kind == 'succeed':
                return (new_cost, next)
            visited.add(uniq_key)
            q.put_nowait((new_cost + next.goal_estimate(), new_cost, next))

def parse(lines):
    maze = list(lines)
    pickups = set([])
    for y, line in enumerate(maze):
        for x, c in enumerate(line):
            if c == '0':
                start = (y, x)
            elif c in '123456789':
                pickups.add((y, x))
    return Node(maze, start, sets.ImmutableSet(pickups))

if __name__ == '__main__':
    root = parse(line.rstrip() for line in sys.stdin)
    (cost, node) = search(root)
    print cost
