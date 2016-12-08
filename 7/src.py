import sys
import re
import itertools as i
import six

class IP:
    pass

def chunks(n, input):
    for i in range(0, len(input), n):
        yield input[i:i + n]

def parse_ip(line):
    ret = IP()
    (ret.supers, ret.hypers) = six.moves.zip_longest(
        *chunks(2, re.split(r'[][]', line)), fillvalue='')
    return ret

def contains_abba(ip_part):
    return re.search(r'(.)((?!\1).)\2\1', ip_part)

def accepts_tls(ip):
    return (any(contains_abba(super) for super in ip.supers)
            and not any(contains_abba(hyper) for hyper in ip.hypers))

aba_re = re.compile(r'(.)((?!\1).)(\1)')

def abas(s):
    for i, _ in enumerate(s):
        m = aba_re.match(s, i)
        if m:
            yield ''.join(m.groups())

def invert(aba):
    return ''.join([aba[1], aba[0], aba[1]])

def accepts_ssl(ip):
    bab_searches = map(invert, i.chain(*map(abas, ip.supers)))
    for bab in bab_searches:
        if any(bab in x for x in ip.hypers):
            return True
    return False

if __name__ == '__main__':
    tls = 0
    ssl = 0
    for line in sys.stdin:
        ip = parse_ip(line.rstrip())
        if accepts_tls(ip):
            tls = tls + 1
        if accepts_ssl(ip):
            ssl = ssl + 1
    print (tls, ssl)
