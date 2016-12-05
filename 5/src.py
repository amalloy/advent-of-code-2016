import sys
from itertools import islice, imap, ifilter, count
import hashlib

class Cracker:
    def __init__(self):
        self.pw1 = ""
        self.pw2 = ['X'] * 8

    def update(self, (i, c)):
        if len(self.pw1) < 8:
            self.pw1 = self.pw1 + c
        if i < '8' and self.pw2[int(i)] == 'X':
            self.pw2[int(i)] = c
        self.progress()

    def progress(self):
        print "part1: %s, part2: %s" % (self.pw1, ''.join(self.pw2))

    def ready(self):
        return len(self.pw1) == 8 and not 'X' in self.pw2

def door_hash(s):
    return hashlib.md5(s).hexdigest()

def valid(s):
    return s.startswith('00000')

def password_part(s):
    return (s[5], s[6])

def password(salt):
    for i in count(0):
        s = salt + str(i)
        candidate = door_hash(s)
        if valid(candidate):
            yield password_part(candidate)


if __name__ == '__main__':
    door = sys.stdin.next().rstrip()
    passwords = Cracker()
    for update in password(door):
        passwords.update(update)
        if passwords.ready():
            break
