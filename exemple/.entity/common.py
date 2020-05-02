@mind
def think(self, this):
    def _think(*args, **kwargs):
        print (f"{repr(self.me)}:", *args, **kwargs)
    return _think