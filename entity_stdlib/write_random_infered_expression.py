from random import choice
from sys import stdout
assert hasattr(mind, 'inference_table'), 'infered_expression: Entity has no inference_table'

if 'expression_writer_opts' in locals().keys():
    origin, token = random_infer(**expression_writer_opts['random_infer_opts'])
else:
    origin, token = random_infer()

if origin == 'builtins':
    res = token
    typ = 'expression'
elif origin == 'infered_entity':
    res = 'mind.me.' + token
    typ = 'expression'
elif origin == 'infered_mind':
    res = 'mind.' + token
    typ = 'expression'
elif origin == 'mind_scope':
    res = token
    typ = 'expression'
else: assert False, origin

with open(file, 'w') as fd:
    fd.write(f"""print({res})""")

@mind
def result(self): return (typ, res)