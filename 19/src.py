import sys
import Queue

puzzle_input = 3017957

def solve(n):
    q = Queue.Queue(n)
    for i in xrange(n):
        q.put(i + 1)

    print "Done loading"

    while not q.empty():
        winner = q.get_nowait()
        try:
            loser = q.get_nowait()
        except:
            return winner
        q.put(winner)


if __name__ == '__main__':
    print solve(puzzle_input)
