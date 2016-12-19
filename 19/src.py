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


def circle(n):
  first = {'num': 1}
  last = first
  for i in xrange(1, n):
    new = {'num': i + 1}
    last['next'] = new
    last = new
    if i == (n / 2) - 1:
      before_mid = new
  last['next'] = first
  return (n, before_mid)

def solve2((n, before_target)):
  while n > 1:
    target = before_target['next']
    before_target['next'] = target['next'] # skip over target
    if n % 2 == 1:
      before_target = before_target['next']
    n = n - 1
  return before_target['num']

if __name__ == '__main__':
    # print solve(puzzle_input)
    print solve2(circle(puzzle_input))
