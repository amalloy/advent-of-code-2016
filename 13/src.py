import sys

goal = (31, 39)
puzzle_input = 1358

def wall((x, y)):
    arbitrary = puzzle_input + x*x + 3*x + 2*x*y + y + y*y
    return bin(arbitrary).count("1") % 2 == 1

class Node:
    def __init__(self, coord):
        self.coord = coord

    def uniq_key(self):
        return self.coord

    def goal_estimate(self):
        return abs(goal[0] - self.coord[0]) + abs(goal[1] - self.coord[1])

    def evaluate(self):
        if self.coord == goal:
            return 'succeed'
        if wall(self.coord):
            return 'fail'
        return 'progress'

    def nexts(self):
        return ((1, Node((dx + self.coord[0], dy + self.coord[1])))
                for dy in [-1,0,1] for dx in [-1,0,1]
                if abs(dy + dx) == 1)

def search(root):
    q = Queue.PriorityQueue()
    visited = set([])
    q.put((0 + root.goal_estimate(), 0, root))
    iterations = 0
    while not q.empty():
        (estimated_cost, spent_cost, node) = q.get()
        iterations = iterations + 1
        if iterations % 1 == 5000:
            print "Moved %d so far, about %d from goal" % (spent_cost, estimated_cost)
        for (spend, next) in node.nexts():
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

if __name__ == '__main__':
    print search(Node((1,1)))
