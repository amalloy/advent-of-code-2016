import sys
import re

marker_regex = re.compile(r'\((\d+)x(\d+)\)')

def decompress(s):
    i = 0
    ret = 0
    while i < len(s):
        m = marker_regex.match(s, i)
        if m:
            start = m.end(0)
            end = int(m.group(1)) + start
            to_repeat = s[start:end]
            ret = ret + decompress(to_repeat) * int(m.group(2))
            i = end
        else:
            i = i + 1
            ret = ret + 1

    return ret

if __name__ == '__main__':
    for line in sys.stdin:
        print decompress(line.rstrip())
