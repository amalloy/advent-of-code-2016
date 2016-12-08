import sys
import regex

class Rect:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows

class Row:
    def __init__(self, row, amt):
        self.row = row
        self.amt = amt

class Col:
    def __init__(self, col, amt):
        self.col = col
        self.amt = amt

instr_regex = regex.compile(r"""(?|(rect)\ (\d+)x(\d+) # use same group numbers in each | branch
                                  | rotate\ (row)\ y=(\d+)\ by\ (\d+)
                                  | rotate\ (column)\ x=(\d+)\ by\ (\d+))""",
                            regex.VERBOSE)

parse_table = {"rect": Rect, "row": Row, "column": Col}
def parse(line):
    match = regex.match(instr_regex, line).groups()
    print match
    return parse_table[match[0]](*map(int, match[1:]))

if __name__ == 'main':
    for line in sys.stdin:
        print parse(line.rstrip())
    print "done"
