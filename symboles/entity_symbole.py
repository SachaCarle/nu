from entity import Entity

print (Entity)

class SymboleEntity(Entity):
    def __get__(self, *args):
        print ("GETT", self, args)
        return self
    def __set__(self, *args):
        print ("SETT", self, args)
        return self
    pass