import sys

dirs = [(1,0), (0, 1), (-1, 0), (0, -1)]
turns = {'L': 1, 'R': -1}

class Position:
    def __init__(self):
        self.heading = 0
        self.location = (0, 0)

    def turn(self, turn):
        self.heading = (self.heading + turns[turn]) % 4

    def walk(self, distance):
        (x, y) = dirs[self.heading]
        (a, b) = self.location
        self.location = (a + x * distance, b + y * distance)

    def apply_command(self, (dir, dist)):
        self.turn(dir)
        self.walk(dist)

def parse_command(s):
    return (s[0], int(s[1:]))

def parse_line(s):
    return (parse_command(x) for x in s.split(", "))

def manhattan_distance((x, y)):
    return abs(x) + abs(y)

if __name__ == '__main__':
    for line in sys.stdin:
        pos = Position()
        part2 = None
        visited = set()
        for (dir, dist) in parse_line(line):
            pos.turn(dir)
            for i in xrange(dist): # so we can record intermediate locations
                pos.walk(1)
                if not part2:
                    if pos.location in visited:
                        part2 = pos.location
                    else:
                        visited.add(pos.location)
        print manhattan_distance(pos.location), manhattan_distance(part2)
