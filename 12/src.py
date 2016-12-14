import sys
import regex
import parsec

class Cpy:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __repr__(self):
        return 'cpy %s %s' % (self.src, self.dst)

class Inc:
    def __init__(self, reg):
        self.reg = reg

    def __repr__(self):
        return 'inc %s' % self.reg

class Dec:
    def __init__(self, reg):
        self.reg = reg

    def __repr__(self):
        return 'dec %s' % self.reg

class Jnz:
    def __init__(self, reg, offset):
        self.reg = reg
        self.offset = offset

    def __repr__(self):
        return 'jnz %s %s' % (self.reg, self.offset)

class Literal:
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return '[lit %d]' % self.val

class Register:
    def __init__(self, reg):
        self.reg = reg

    def __repr__(self):
        return '[reg %s]' % self.reg

class Computer:
    pass

parse_value = parsec.choice(parsec.letter().parsecmap(Register),
                            parsec.regex(r'-?\d+').parsecmap(int).parsecmap(Literal))
parse_args = parsec.separated(parse_value, parsec.space(), 1, maxt=2)
instructions = {'cpy': Cpy, 'inc': Inc, 'dec': Dec, 'jnz': Jnz}
parse_instr = reduce(parsec.choice, [parsec.string(k).result(v) for (k, v) in instructions.items()])

def apply_args(ctor):
    return (parsec.space()
            .compose(parse_args.parsecmap(lambda args: ctor(*args))))
parse_line = parse_instr.bind(apply_args)

if __name__ == '__main__':
    for line in sys.stdin:
        print parse_line.parse(line.rstrip())
