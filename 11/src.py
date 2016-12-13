import sys
import itertools
import Queue

def combine_interactions(a, b):
    if a == 'fix' or b == 'fix':
        return 'fix'
    if a == 'break' or b == 'break':
        return 'break'
    return 'neutral'

class RTG:
    def __init__(self, metal):
        self.metal = metal

    def broken(self, room):
        return False

    def interact(self, metal):
        if metal == self.metal:
            return 'fix'
        return 'break'

    def __repr__(self):
        return "RTG('%s')" % self.metal

    def __key(self):
        return (self.metal,)

    def __hash__(self):
        return self.__key().__hash__()

    def __eq__(self, other):
        return isinstance(other, RTG) and self.__key() == other.__key()

class Chip:
    def __init__(self, metal):
        self.metal = metal

    def broken(self, room):
        breaking = 'neutral'
        for obj in room.objs:
            breaking = combine_interactions(breaking, obj.interact(self.metal))
        return breaking == 'break'

    def interact(self, metal):
        return 'neutral'

    def __repr__(self):
        return "Chip('%s')" % self.metal

    def __key(self):
        return (self.metal,)

    def __hash__(self):
        return self.__key().__hash__()

    def __eq__(self, other):
        return isinstance(other, Chip) and self.__key() == other.__key()

class Room:
    def __init__(self, objs):
        self.objs = objs

    def legal(self):
        return not any(obj.broken(self) for obj in self.objs)

    def add(self, objs):
        return Room(self.objs + objs)

    def remove(self, objs):
        return Room(list(set(self.objs) - set(objs)))

    def possible_removals(self):
        return ([[x] for x in self.objs]
                + list(itertools.imap(list, itertools.combinations(self.objs, 2))))

    def empty(self):
        return not self.objs

    def __repr__(self):
        return "Room(%s)" % repr(self.objs)

    def __key(self):
        return tuple(sorted(self.objs))

    def __hash__(self):
        return self.__key().__hash__()

    def __eq__(self, other):
        return self.__key() == other.__key()

class Node:
    def __init__(self, rooms, elevator):
        self.rooms = rooms
        self.elevator = elevator

    def evaluate(self):
        if not all(r.legal() for r in self.rooms):
            return 'fail'
        if all(r.empty() for r in self.rooms[:-1]):
            return 'succeed'
        return 'progress'

    def goal_estimate(self):
        return sum((len(self.rooms) - i - 1) * 2 * max(0, len(room.objs) - 1)
                   for i, room in enumerate(self.rooms))

    def nexts(self):
        i = self.elevator
        r = self.rooms[i]
        dests = []
        if i != 0:
            dests.append(i - 1)
        if i < len(self.rooms) - 1:
            dests.append(i + 1)
        for removals in r.possible_removals():
            new_room = self.rooms[i].remove(removals)
            for dest in dests:
                rooms = list(self.rooms)
                rooms[i] = new_room
                rooms[dest] = self.rooms[dest].add(removals)
                yield (1,
                       'move %s from floor %d to floor %d' % (repr(removals), i, dest),
                       Node(rooms, dest))

    def __repr__(self):
        return "Node(%s, %d)" % (repr(self.rooms), self.elevator)

    def __key(self):
        return (tuple(self.rooms), self.elevator)

    def __hash__(self):
        return self.__key().__hash__()

    def __eq__(self, other):
        return self.__key() == other.__key()

def search(root):
    q = Queue.PriorityQueue()
    visited = set([])
    q.put((0 + root.goal_estimate(), 0, [], root))
    iterations = 0
    while not q.empty():
        (estimated_cost, spent_cost, path, node) = q.get()
        iterations = iterations + 1
        if iterations % 1 == 5000:
            print "Moved %d so far, about %d from goal" % (spent_cost, estimated_cost)
        for (spend, edge, next) in node.nexts():
            if next in visited:
                continue
            kind = next.evaluate()
            if kind == 'fail':
                continue
            new_cost = spent_cost + spend
            new_path = path + [edge]
            if kind == 'succeed':
                return (new_cost, new_path, next)
            visited.add(next)
            q.put_nowait((new_cost + next.goal_estimate(), new_cost, new_path, next))

# The first floor contains a thulium generator, a thulium-compatible microchip, a plutonium generator, and a strontium generator.
# The second floor contains a plutonium-compatible microchip and a strontium-compatible microchip.
# The third floor contains a promethium generator, a promethium-compatible microchip, a ruthenium generator, and a ruthenium-compatible microchip.
# The fourth floor contains nothing relevant.
root = Node([Room([RTG('thulium'), Chip('thulium'), RTG('plutonium'), RTG('strontium'),
                   RTG('elerium'), Chip('elerium'), RTG('dilithium'), Chip('dilithium')]),
             Room([Chip('plutonium'), Chip('strontium')]),
             Room([RTG('promethium'), Chip('promethium'), RTG('ruthenium'), Chip('ruthenium')]),
             Room([])],
            0)

if __name__ == '__main__':
    print search(root)[0]
