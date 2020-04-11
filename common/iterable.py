class Iterable:
    def __init__(self, fun):
        self.fun = fun
        self.__name__ = fun.__name__
    def __iter__(self):
        return iter(self.fun())

def fun_iterable(fun):
    return Iterable(fun)
