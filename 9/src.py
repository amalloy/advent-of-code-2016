import sys
import re

marker_regex = re.compile(r'\((\d+)x(\d+)\)')

def decompress(s):
    i = 0
    while i < len(s):
        m = marker_regex.match(s, i)
        if m:
            start = m.end(0)
            end = int(m.group(1)) + start
            to_repeat = s[start:end]
            for _ in range(int(m.group(2))):
                yield to_repeat
            i = end
        else:
            yield s[i]
            i = i + 1

if __name__ == '__main__':
    for line in sys.stdin:
        print sum(len(s) for s in decompress(line.rstrip()))
