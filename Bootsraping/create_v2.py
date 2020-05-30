from entity import Location

ns = Location('NUSYSTEM')('watchdog')

@ns.receive('created', ns)
def mod(*args):
    print (*args)


from nu_entity import ScopeInstance, EntityInstance

e = EntityInstance(any='None')

print (e.__dict__.keys())


e.__exec__(f"""

print ('lol')

print (type(globals()))

print (any)

def exemple(obj):
    assert isinstance(obj, bool)
    return obj

exemple = True

print (exemple)


class NUSYSTEM:
    pass

print (home)
print (NUSYSTEM)
NUSYSTEM.__exec__(f"print(home)")

import os

os.chdir('D://synaps//')

print(os.getcwd())







""")

exit()
exec("""

print (repr(symbole))
print (repr(symbole.lol))
print (repr(symbole.lol.mdr))

print (repr(symbole('exemple')))
print (repr(symbole.lol('exemple')))
print (repr(symbole.lol.mdr('exemple')))

print (repr(symbole))
print (repr(symbole(exemple).lol))

print (repr(symbole('exemple').lol))
print (repr(symbole.lol('exemple').mdr(lol)))
print (repr(symbole.lol.mdr('exemple').lolz))

print(repr(exemple(8, 9, 10, anb=lolz)))

print(repr(exemple(8, print, 10, anb=lolz)))

print (globals().keys())



exit()
def test():
    print (lol)
lol = None









""", ScopeInstance())















from time import sleep
sleep(30)
#!