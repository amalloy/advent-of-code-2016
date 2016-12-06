import sys

if __name__ == '__main__':
    freqs = [{} for _ in range(8)]
    for line in sys.stdin:
        for i, c in enumerate(line.rstrip()):
            freqs[i][c] = freqs[i].get(c, 0) + 1

    for f in [max, min]:
        print "".join([f(m.items(), key=lambda x: x[1])[0] for m in freqs])
