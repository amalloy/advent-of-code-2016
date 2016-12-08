import sys
import re

def ip_parts(line):
    return filter(len, re.split(r'[][]', line))

def contains_abba(ip_part):
    return re.search(r'(.)((?!\1).)\2\1', ip_part)

def accepts_tls(ip):
    has_abba = False
    want_abba = True
    while ip:
        if contains_abba(ip[0]):
            if want_abba:
                has_abba = True
            else:
                return False
        ip = ip[1:]
        want_abba = not want_abba
    return has_abba

if __name__ == '__main__':
    valid = 0
    for line in sys.stdin:
        if (accepts_tls(ip_parts(line.rstrip()))):
            valid = valid + 1
    print valid
