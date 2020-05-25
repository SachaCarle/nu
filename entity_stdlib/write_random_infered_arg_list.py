from random import choice
from sys import stdout
assert hasattr(mind, 'inference_table')

opts = {}
for k in ['expression_writer_opts']:
    if k in locals():
        opts[k] = locals()[k]

if choice((True, False)):
    mind(expression_writer, file=file, **opts)
    typ, expr = mind.me.result
    assert typ == 'expression', typ
    res = expr

    while choice((True, False)):
        mind(expression_writer, file=file, **opts)
        typ, expr = mind.me.result
        assert typ == 'expression', typ
        res += ', ' + expr
else:
    res = ''
typ = 'arg_list'
with open(file, 'w') as fd:
    fd.write(f"""{res}""")
@mind
def result(self): return (typ, res)