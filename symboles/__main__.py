from symboles import Symbole

sym = Symbole('sym')
sub = Symbole('sub')
ter = Symbole('ter')
quart = Symbole('quart')

print (sym)
print (sym.sub)
print (sym.ter)
print (sym.sub.ter)
print (sym.sub.ter.quart)


print (sym.sym)
print (quart.sym)
print (ter.sym)

unknow = ter.sub
print (unknow)
print (unknow.sym)


class Ob:
    why = quart
    pass

o = Ob()
o.what = sym

print ("!", o.what)
print ("!", o.what.sub)

print ("!", o.why)
print ("!", o.why.sub)







print ()