import sys
import regex
import parsec

class Cpy:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def apply(self, computer):
        regs = computer.registers
        self.dst.write(regs, self.src.eval(regs))

    def toggle(self):
        return Jnz(self.src, self.dst)

    def __repr__(self):
        return 'cpy %s %s' % (self.src, self.dst)

class Inc:
    def __init__(self, reg):
        self.reg = reg

    def apply(self, computer):
        regs = computer.registers
        self.reg.write(regs, 1 + self.reg.eval(regs))

    def toggle(self):
        return Dec(self.reg)

    def __repr__(self):
        return 'inc %s' % self.reg

class Dec:
    def __init__(self, reg):
        self.reg = reg

    def apply(self, computer):
        regs = computer.registers
        self.reg.write(regs, self.reg.eval(regs) - 1)

    def toggle(self):
        return Inc(self.reg)

    def __repr__(self):
        return 'dec %s' % self.reg

class Jnz:
    def __init__(self, arg, offset):
        self.arg = arg
        self.offset = offset

    def apply(self, computer):
        regs = computer.registers
        if self.arg.eval(regs) != 0:
            computer.ip = computer.ip + self.offset.eval(regs) - 1

    def toggle(self):
        return Cpy(self.arg, self.offset)

    def __repr__(self):
        return 'jnz %s %s' % (self.arg, self.offset)

class Tgl:
    def __init__(self, offset):
        self.offset = offset

    def apply(self, computer):
        target = computer.ip + self.offset.eval(computer.registers)
        if target != computer.ip and target >= 0 and target < len(computer.program):
            computer.program[target] = computer.program[target].toggle()

    def toggle(self):
        return Inc(self.offset)

    def __repr__(self):
        return 'tgl %s' % self.offset

# pseudo-instructions used as optimization targets
class Opt:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def apply(self, computer):
        regs = computer.registers
        self.dst.write(regs, self.invoke(self.src.eval(regs), self.dst.eval(regs)))
        self.src.write(regs, 0)

class Add(Opt):
    def invoke(self, a, b):
        return a + b

class Mul(Opt):
    def invoke(self, a, b):
        return a * b

class Literal:
    def __init__(self, val):
        self.val = val

    def eval(self, registers):
        return self.val

    def write(self, registers, value):
        pass # Tgl has made this literal appear in an invalid place

    def __repr__(self):
        return '[lit %d]' % self.val

class Register:
    def __init__(self, reg):
        self.reg = reg

    def eval(self, registers):
        return registers[self.reg]

    def write(self, registers, value):
        registers[self.reg] = value

    def __repr__(self):
        return '[reg %s]' % self.reg

class Computer:
    def __init__(self, program, registers):
        self.program = program
        self.registers = registers
        self.ip = 0

    def run_program(self):
        while self.ip < len(self.program):
            self.program[self.ip].apply(self)
            self.ip = self.ip + 1

parse_value = parsec.choice(parsec.letter().parsecmap(Register),
                            parsec.regex(r'-?\d+').parsecmap(int).parsecmap(Literal))
parse_args = parsec.separated(parse_value, parsec.space(), 1, maxt=2)
instructions = {'cpy': Cpy, 'inc': Inc, 'dec': Dec, 'jnz': Jnz, 'tgl': Tgl}
parse_instr = reduce(parsec.choice, [parsec.string(k).result(v) for (k, v) in instructions.items()])

def apply_args(ctor):
    return (parsec.space()
            .compose(parse_args.parsecmap(lambda args: ctor(*args))))
parse_line = parse_instr.bind(apply_args)

def regex_parse(line):
  def arg(x):
    m = regex.match(r'-?\d+', x)
    if m:
      return Literal(int(x))
    return Register(x)

  m = regex.match(r'cpy (-?\d+|[a-d]) ([a-d])', line)
  if m:
    return Cpy(arg(m.group(1)), Register(m.group(2)))
  m = regex.match(r'inc ([a-d])', line)
  if m:
    return Inc(Register(m.group(1)))
  m = regex.match(r'dec ([a-d])', line)
  if m:
    return Dec(Register(m.group(1)))
  m = regex.match(r'jnz (-?\d+|[a-d]) (-?\d+|[a-d])', line)
  return Jnz(arg(m.group(1)), arg(m.group(2)))

if __name__ == '__main__':
    instrs = [parse_line.parse(line.rstrip()) for line in sys.stdin]
    regs = {k: 0 for k in 'abcd'}
    regs['a'] = 7

    cpu1 = Computer(list(instrs), regs)
    cpu1.run_program()
    print cpu1.registers['a']

    regs = {k: 0 for k in 'abcd'}
    regs['a'] = 12

    cpu2 = Computer(list(instrs), regs)
    cpu2.run_program()
    print cpu2.registers['a']
