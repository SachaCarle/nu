from parse import parse

def rule(tx):
    def _rule(fun):
        def get_line(line):
            r = parse(tx, line)
            if r is None:
                return False
            return fun(r)
        return get_line
    return _rule

@rule("{:d}{tail}")
def number(res):
    return res
@rule("{:l}{tail}")
def letter(res):
    return res

def parse_line(line):
    ld = line.decode('utf-8')
    r = number(ld)
    r = letter(ld)
    print (r)

f = open("test.py", "rb", buffering=0)
for l in f:
    r = parse_line(l)
