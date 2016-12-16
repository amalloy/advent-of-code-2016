import sys
import itertools
import re
from md5 import md5

puzzle_input = 'yjdafjpo'

def basic_hash(n):
  return md5(puzzle_input + str(n)).hexdigest()

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

if __name__ == '__main__':
  part1 = otp_keys(1000, basic_hash)
  print itertools.islice(part1, 63, 64).next()
