import sys
import regex

class Rect:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows

    def transform(self, _g):
        return [(y, x, '#') for y in range(self.rows) for x in range(self.cols)]

class Row:
    def __init__(self, row, amt):
        self.row = row
        self.amt = amt

    def transform(self, g):
        return [(self.row, (x + self.amt) % g.width, g.grid[self.row][x]) for x in range(g.width)]

class Col:
    def __init__(self, col, amt):
        self.col = col
        self.amt = amt

    def transform(self, g):
        return [((y + self.amt) % g.height, self.col, g.grid[y][self.col]) for y in range(g.height)]

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [['.'] * width for _ in range(height)]

    def render(self):
        for line in self.grid:
            print "".join(line)

    def apply(self, transformation):
        for (y, x, c) in transformation:
            self.grid[y][x] = c

instr_regex = regex.compile(r"""(?|(rect)\ (\d+)x(\d+) # use same group numbers in each | branch
                                  | rotate\ (row)\ y=(\d+)\ by\ (\d+)
                                  | rotate\ (column)\ x=(\d+)\ by\ (\d+))""",
                            regex.VERBOSE)

parse_table = {"rect": Rect, "row": Row, "column": Col}
def parse(line):
    match = regex.match(instr_regex, line).groups()
    return parse_table[match[0]](*map(int, match[1:]))

if __name__ == '__main__':
    g = Grid(50 ,6)
    for line in sys.stdin:
        g.apply(parse(line.rstrip()).transform(g))

    print sum(1 for y in range(g.height) for x in range(g.width) if g.grid[y][x] == '#')
    g.render()
