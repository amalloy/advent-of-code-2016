import sys

keypad = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
deltas = {'U': (-1, 0), 'D': (1, 0), 'R': (0, 1), 'L': (0, -1)}

def clamp((y, x)):
    if (y < 0):
        y = 0
    if (y > 2):
        y = 2
    if (x < 0):
        x = 0
    if (x > 2):
        x = 2
    return (y, x)

def move((y, x), dir):
    (dy, dx) = deltas[dir]
    return clamp((y + dy, x + dx))

if __name__ == '__main__':
    pos = (1, 1)
    for line in sys.stdin:
        for dir in line.rstrip():
            pos = move(pos, dir)
        print keypad[pos[0]][pos[1]]
