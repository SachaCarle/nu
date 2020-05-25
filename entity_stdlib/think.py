@mind
def think(self):
    def _think(*args, **kwargs):
        print (f"{repr(self.me)}:", *args, **kwargs)
    return _think