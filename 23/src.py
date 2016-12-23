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
            computer.deoptimize()
            computer.program[target] = computer.program[target].toggle()
            computer.optimize()

    def toggle(self):
        return Inc(self.offset)

    def __repr__(self):
        return 'tgl %s' % self.offset

# pseudo-instructions used as optimization targets
class Opt:
    def __init__(self, dst, srcs):
        self.dst = dst
        self.srcs = srcs

    def apply(self, computer):
        regs = computer.registers
        self.dst.write(regs, self.dst.eval(regs) +
                       reduce(lambda x, y: x * y.eval(regs), self.srcs, 1))
        for src in self.srcs:
            src.write(regs, 0)

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
        self.optimize()
        self.registers = registers
        self.ip = 0

    def deoptimize(self):
        self.program = self.real_program

    def optimize(self):
        self.real_program = self.program
        self.program = optimize_multiplication_loops(optimize_addition_loops(list(self.program)))

    def run_program(self):
        while self.ip < len(self.program):
            self.program[self.ip].apply(self)
            self.ip = self.ip + 1

def optimize_addition_loops(program):
    i = 0
    while i < len(program) - 2:
        (op1, op2, op3) = program[i:i+3]
        if isinstance(op1, Dec) and isinstance(op2, Inc):
            (op1, op2) = (op2, op1)
        if isinstance(op1, Inc) and isinstance(op2, Dec) and isinstance(op3, Jnz):
            try: # just assume argument types line up, continue on exception
                if op3.offset.val == -2 and op3.arg.reg == op2.reg.reg:
                    program[i:i+3] = ([Opt(op1.reg, [op2.reg])] +
                                      [Jnz(Literal(0), Literal(0))] * 2)
                    i = i + 2
            except:
                pass
        i = i + 1

    return program

def optimize_multiplication_loops(program):
    i = 0
    while i < len(program) - 4:
        (op1, _, _, op4, op5) = program[i:i+5]
        if isinstance(op1, Opt) and isinstance(op4, Dec) and isinstance(op5, Jnz):
            try: # just assume argument types line up, continue on exception
                if len(op1.srcs) == 1 and op5.offset.val == -5 and op5.arg.reg == op4.reg.reg:
                    program[i:i+5] = ([Opt(op1.dst, op1.srcs + [op5.arg])] +
                                      [Jnz(Literal(0), Literal(0))] * 4)
                    i = i + 4
            except:
                print "failed to optimize multiplication of %s" % program[i:i+5]
        i = i + 1

    return program


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
