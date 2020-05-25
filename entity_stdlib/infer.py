from random import choice

@mind
def random_infer(self):
    def random_infer(**opts):
        assert hasattr(mind, 'inference_table')
        ok = False
        while not ok:
            r = choice(list(mind.inference_table.keys()))
            ok = True
            if r in opts.keys():
                ok = opts[r]
            if len(mind.inference_table[r]) <= 0:
                ok = False
        return (r, choice(mind.inference_table[r]))
    return random_infer





#!