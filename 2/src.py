import sys

keypads = ([[1,2,3],
            [4,5,6],
            [7,8,9]],
           [[0,0,1,0,0],
            [0,2,3,4,0],
            [5,6,7,8,9],
            [0,'A','B','C',0],
            [0,0,'D',0,0]])

deltas = {'U': (-1, 0), 'D': (1, 0), 'R': (0, 1), 'L': (0, -1)}

def move((y, x), dir, keypad):
    (dy, dx) = deltas[dir]
    ret = (y + dy, x + dx)
    if (0 <= ret[0] < len(keypad)
        and 0 <= ret[1] < len(keypad)
        and keypad[ret[0]][ret[1]] != 0):
        return ret
    return (y, x)

if __name__ == '__main__':
    locs = [(1, 1), (2, 0)]
    for line in sys.stdin:
        for dir in line.rstrip():
            locs = [move(loc, dir, keypads[i]) for i, loc in enumerate(locs)]
        print [keypads[i][loc[0]][loc[1]] for i, loc in enumerate(locs)]
