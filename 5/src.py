import sys
from itertools import islice, imap, ifilter, count
import hashlib

def door_hash(s):
    return hashlib.md5(s).hexdigest()

def valid(s):
    return s.startswith('00000')

def password_part(s):
    return s[5]

def password(salt):
    for i in count(0):
        s = salt + str(i)
        candidate = door_hash(s)
        if valid(candidate):
            yield password_part(candidate)


if __name__ == '__main__':
    door = sys.stdin.next().rstrip()
    print "".join(list(islice(password(door), 0, 8)))
