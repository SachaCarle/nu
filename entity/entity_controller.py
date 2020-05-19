from .entity_class import Entity

class Controller(Entity):
    def __call__(self, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return self.console()
        else:
            return Entity.__call__(self, *args, **kwargs)
    def ask(self): return input("$> ")
    def console(self):
        while True:
            command = self.ask()
            if command == "exit":
                break
            else:
                self.exec(command)
    def exec(self, s):
            if s == 'help':
                print (f"""\t{repr(self)}:
MIND: {' '.join(self.__mind__.keys())}""")
            elif s in "           \t \t  \t  \t\n\n\n\t\n":
                pass
            else:
                rs = []
                for s in s.split(' '):
                    if not (s in self.__mind__) and not (s.startswith('!') and s[1:] in self.__mind__ ):
                        print (s + " not in " + repr(self))
                        r = s
                    elif s.startswith('!'):
                        r = self.__mind__[s[1:]]
                        print ('fun:', r)
                        rs = [r(*rs)]
                        r = rs
                    else:
                        r = self.__mind__[s]
                    rs.append(r)
                print (rs)
                return rs

