from random import choice as _choice

class Iterable:
    def __init__(self, fun):
        self.fun = fun
        self.__name__ = fun.__name__
    def __iter__(self):
        return iter(self.fun())

def fun_iterable(fun):
    return Iterable(fun)

def choice(x):
    try:
        return _choice(list(x))
    except Exception as e:
        raise Exception(f'RAISED BY {str(x)}')