class ComposedSymbole:

    def __init__(self, a, b):
        self.__parent__ = a
        self.__this__ = b

    def __str__(self):
        return str(self.__parent__) + '.' + str(self.__this__)

    def __getattribute__(self, key):
        if key.startswith('__') and key.endswith('__'):
            return object.__getattribute__(self, key)
        return ComposedSymbole(self, self.__this__.__class__(key))

        #!