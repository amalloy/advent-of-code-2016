import sys
import re

class Bot:
    def __init__(self, graph, id, rule):
        self.graph = graph
        self.id = id
        self.rule = rule
        self.num = None

    def receive(self, n):
        if self.num is None:
            self.num = n
        else:
            if n < self.num:
                (n, self.num) = (self.num, n)
            if n == 61 and self.num == 17:
                print "bot %d handles 61 and 17" % self.id
            self.graph[self.rule['hi']].receive(n)
            self.graph[self.rule['lo']].receive(self.num)
            self.num = None

    def contents(self):
        if self.num:
            return [self.num]
        return []

class Output:
    def __init__(self, graph, id):
        self.graph = graph
        self.id = id
        self.outputs = []

    def receive(self, n):
        self.outputs.append(n)

    def contents(self):
        return self.outputs

def default_output(graph, kind, num):
    num = int(num)
    k = (kind, num)
    graph[k] = graph.get(k, Output(graph, num))
    return k

def run_graph(lines):
    graph = {}
    inputs = []
    for line in lines:
        value_match = re.match(r'value (\d+) goes to bot (\d+)', line)
        if value_match:
            inputs.append((int(value_match.group(2)), int(value_match.group(1))))
            continue
        rule_match = re.match(r'bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)', line)
        id = int(rule_match.group(1))
        graph[('bot', id)] = Bot(graph, id, {'lo': default_output(graph, rule_match.group(2), int(rule_match.group(3))),
                                             'hi': default_output(graph, rule_match.group(4), int(rule_match.group(5)))})

    for (id, num) in inputs:
        graph[('bot', id)].receive(num)

    print reduce(lambda x, y: x * y, [graph[('output', i)].contents()[0] for i in range(3)], 1)


if __name__ == '__main__':
    run_graph(line.rstrip() for line in sys.stdin)
