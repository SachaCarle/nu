# OPEN CLASS_SCOPE
class Scope(dict):
    def __init__(self):
        dict.__init__(self)
    def __setitem__(self, key, value):
        raise Exception('Nuthon interpreter does not allow void creation.' + f"""
key = {key}\nvalue = {repr(value)}""")
# CLOSE CLASS_SCOPE