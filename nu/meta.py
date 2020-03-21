import collections

class NuException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args)

class NuObject(collections.MutableMapping):
    def __str__(self):
        return dict.__str__(self.store)
    def __repr__(self):
        return f"""<{dict.__repr__(self.store)}>"""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getattr__(self, key):
        if key == "store":
            return object.__getattribute__(self, key)
        if not (self.__keytransform__(key) in self.store.keys()):
            raise NuException('KeyNotFound', key)
        return self.store[self.__keytransform__(key)]

    def __setattr__(self, key, value):
        if key == "store":
            return object.__setattr__(self, key, value)
        self.store[self.__keytransform__(key)] = value

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value


    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key



def obj(*args, **kwargs):
    return NuObject(*args, **kwargs)