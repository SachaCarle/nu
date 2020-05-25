
if not 'target_mind' in locals():
    target_mind = mind

infered_mind = [o for o in dir(target_mind) if not (o.startswith('__') and o.endswith('__'))]
infered = [o for o in dir(target_mind.me) if not (o.startswith('__') and o.endswith('__'))]

ds = [o for o in list(__builtins__.keys()) if not (o.startswith('__') and o.endswith('__'))]


res = {
    'builtins': ['mind', *ds, '__any_id__'],
    'mind_scope': [*target_mind.keys()],
    'infered_mind': infered_mind,
    'infered_entity': infered,
}

mind.inference_table = res
with open(file, 'w') as fd:
    fd.write(f"""{res}""")
