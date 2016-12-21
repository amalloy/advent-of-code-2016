import sys
import re

class Swap:
    def __init__(self, f):
        self.f = f

    def transform(self, s):
        (x, y) = self.f(s)
        return [(x, s[y]), (y, s[x])]

    def undo(self, s):
        return self.transform(s)

class Rotation:
    def __init__(self, f):
        self.f = f

    def transform(self, s):
        amt = self.f(s)
        return [((i + amt) % len(s), s[i]) for i in xrange(len(s))]

    # very gross to have undo depend on apply. in principle i think this
    # could be done by calculating, based on where the looked-for character
    # ended up, the unique place it must have come from; but it's hard.
    # also, we'd have to undo the lambda-based approach in favor of two
    # different classes, PositionalRotation and LetterRotation or something.
    def undo(self, s):
        for i in xrange(len(s)):
            speculative = Rotation(lambda _: i)
            inverse_transform = speculative.transform(s)
            transformed = apply(s, inverse_transform)
            undone = apply(transformed, self.transform(transformed))
            if undone == s:
                return inverse_transform

class Reversal:
    def __init__(self, x, y):
        self.x = x
        self.n = y - x + 1

    def transform(self, s):
        return [(i+ self.x, s[self.n + self.x - i - 1]) for i in xrange(self.n)]

    def undo(self, s):
        return self.transform(s)

class Move:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def transform(self, s):
        if self.x < self.y:
            shift = [(i, s[i + 1]) for i in xrange(self.x, self.y)]
        else:
            shift = [(i, s[i - 1]) for i in xrange(self.x, self.y, -1)]
        return [(self.y, s[self.x])] + shift

    def undo(self, s):
        return Move(self.y, self.x).transform(s)

def apply(s, transformation):
    ret = s[:]
    for i, x in transformation:
        ret[i] = x
    return ret

def locate(letter):
    def f(s):
        i = s.index(letter)
        if i >= 4:
            i = i + 1
        return i + 1
    return f

def parse(line):
    m = re.match(r'swap position (\d+) with position (\d+)', line)
    if m:
        return Swap(lambda _: tuple(map(int, m.groups())))
    m = re.match(r'swap letter (.) with letter (.)', line)
    if m:
        return Swap(lambda s: (s.index(m.group(1)), s.index(m.group(2))))
    m = re.match(r'rotate (\w+) (\d+) steps?', line)
    if m:
        return Rotation(lambda s: int(m.group(2)) * (1 if m.group(1) == 'right' else -1))
    m = re.match(r'rotate based on position of letter (.)', line)
    if m:
        return Rotation(locate(m.group(1)))
    m = re.match(r'reverse positions (\d+) through (\d+)', line)
    if m:
        return Reversal(*map(int, m.groups()))
    m = re.match(r'move position (\d+) to position (\d+)', line)
    return Move(*map(int, m.groups()))

def parse_with_info(line):
    rule = parse(line)
    rule.explanation = line
    return rule

def update_password(s, rule):
    ret = apply(s, rule.transform(s))
    return ret

def crack_password(s, rule):
    ret = apply(s, rule.undo(s))
    return ret

if __name__ == '__main__':
    rules = [parse_with_info(line.rstrip()) for line in sys.stdin]
    password = list('abcdefgh')
    part1 = reduce(update_password, rules, password)
    print "part1: %s" % "".join(part1)

    part2 = reduce(crack_password, rules[::-1], list('fbgdceah'))
    print "part2: %s" % "".join(part2)
