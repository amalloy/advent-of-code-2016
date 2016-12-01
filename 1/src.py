import sys

dirs = [(1,0), (0, 1), (-1, 0), (0, -1)]

class Position:
    def __init__(self):
        self.heading = 0
        self.location = (0, 0)

    def turn(self, turn):
        if turn == 'R':
            delta = 1
        elif turn == 'L':
            delta = -1
        else:
            raise Exception("invalid direction '%s'" % turn)
        self.heading = (self.heading + delta) % 4

    def walk(self, distance):
        (x, y) = dirs[self.heading]
        (a, b) = self.location
        self.location = (a + x * distance, b + y * distance)

    def applyCommand(self, (dir, dist)):
        self.turn(dir)
        self.walk(dist)

def parseCommand(s):
    return (s[0], int(s[1:]))

def parseLine(s):
    return (parseCommand(x) for x in s.split(", "))

if __name__ == '__main__':
    for line in sys.stdin:
        pos = Position()
        commands = list(parseLine(line))
        for command in commands:
            pos.applyCommand(command)
        (x, y) = pos.location
        print abs(x) + abs(y)
