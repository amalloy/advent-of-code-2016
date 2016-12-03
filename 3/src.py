import sys

if __name__ == '__main__':
    valid = 0
    for line in sys.stdin:
        [a,b,c] = map(int, line.split())
        print [a,b,c]
        if (a + b > c and a+c > b and b+c > a):
            valid = valid + 1
    print valid
