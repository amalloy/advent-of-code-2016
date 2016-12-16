import sys
import itertools
import re
from md5 import md5

puzzle_input = 'yjdafjpo'

def basic_hash(n):
  return md5(puzzle_input + str(n)).hexdigest()

def stretch_hash(cycles):
  def cycle(n):
    ret = basic_hash(n)
    for i in xrange(cycles):
      ret = md5(ret).hexdigest()
    return ret
  return cycle

def otp_keys(horizon, hash_func):
  lookahead = {k: -1 for k in '0123456789abcdef'}
  def update_lookahead(n):
    for quint in re.finditer(r'(.)\1{4}', hash_func(n)):
      lookahead[quint.group(1)] = n
  for i in xrange(1, horizon):
    update_lookahead(i)

  for i in itertools.count():
    update_lookahead(i + horizon)
    triple = re.search(r'(.)\1{2}', hash_func(i))
    if triple:
      if lookahead[triple.group(1)] > i:
        yield i

def solve(hash_func):
  print itertools.islice(otp_keys(1000, hash_func), 63, 64).next()

if __name__ == '__main__':
  solve(basic_hash)
  solve(stretch_hash(2016))
