import sys

keypad = [[0,0,1,0,0],[0,2,3,4,0],[5,6,7,8,9],[0,'A','B','C',0],[0,0,'D',0,0]]
deltas = {'U': (-1, 0), 'D': (1, 0), 'R': (0, 1), 'L': (0, -1)}
valid = {0: {2}, 1: {1,2,3}, 2: set(range(5)), 3: {1,2,3}, 4: {2}}

def move((y, x), dir):
    (dy, dx) = deltas[dir]
    ret = (y + dy, x + dx)
    if ret[1] in valid.get(ret[0], {}):
        return ret
    return (y, x)

if __name__ == '__main__':
    pos = (2, 0)
    for line in sys.stdin:
        for dir in line.rstrip():
            pos = move(pos, dir)
        print keypad[pos[0]][pos[1]]
