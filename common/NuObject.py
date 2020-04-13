import collections

class NuObject(collections.MutableMapping):
    def __call__(self, *args, **kwargs):
        for k, v in kwargs.items():
            self.sub_store[k] = v
        if len(args) == 1:
            return self.sub_store[args[0]]

    def __str__(self):
        return dict.__str__(self.store)
    def __repr__(self, **kwargs):
        return f"""<{dict.__repr__({**self.store, **kwargs})}>"""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.sub_store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return getattr(self, key)
    def __getattr__(self, key):
        if key in ("store", "sub_store"):
            return object.__getattribute__(self, key)
        if not (self.__keytransform__(key) in self.store.keys()):
            raise Exception('KeyNotFound', key)
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        return setattr(self, key, value)
    def __setattr__(self, key, value):
        if key in ("store", "sub_store"):
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
