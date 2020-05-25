from random import choice
from sys import stdout
assert hasattr(mind, 'inference_table')

opts = {}
for k in ['expression_writer_opts']:
    if k in locals():
        opts[k] = locals()[k]


mind(expression_writer, file=file, **opts)
typ, expr = mind.me.result
assert typ == 'expression', typ


mind(arg_list_writer, file=file,
    expression_writer=expression_writer, **opts)
al_typ, al_expr = mind.me.result
assert al_typ == 'arg_list', al_typ

res = expr + "(" + al_expr + ")"
typ = 'expression'
with open(file, 'w') as fd:
    fd.write(f"""print('RESULT=>', {res})""")
@mind
def result(self): return (typ, res)