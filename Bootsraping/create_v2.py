from entity import Location

ns = Location('NUSYSTEM')('watchdog')

@ns.receive('created', ns)
def mod(*args):
    print (*args)


from scope_instance_class import ScopeInstance

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