import sys
from itertools import imap
from collections import Counter


class Room:
    pass

def parse_room(s):
    last_dash = s.rfind("-")
    after_name = s[last_dash+1:]
    bracket = after_name.find("[")
    room = Room()
    room.name = s[:last_dash]
    room.sector = int(after_name[:bracket])
    room.checksum = after_name[bracket+1:-2]
    return room

def frequencies(coll):
    ret = Counter(coll)
    del ret['-']
    return ret

def sort_frequencies(dict):
    def alphasort((a, i), (b, j)):
        if i != j:
            return j - i
        return ord(a) - ord(b)

    return sorted(dict.items(), cmp=alphasort)

def run_checksum(name):
    return ''.join([c for (c, n) in sort_frequencies(frequencies(name))[:5]])

def rotate(amt):
    def rotator(c):
        if c == '-':
            return " "
        x = ord(c) - ord('a')
        return chr((x + amt) % 26 + ord('a'))
    return rotator

if __name__ == '__main__':
    sum = 0
    for room in imap(parse_room, sys.stdin):
        if room.checksum == run_checksum(room.name):
            sum = sum + room.sector
            if ('northpole object storage' ==
                ''.join(map(rotate(room.sector), room.name))):
                print "part 2:", room.sector
    print "part 1:", sum
