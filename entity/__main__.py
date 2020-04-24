from entity import load_physical
import os, sys

primal_location = os.path.join(os.path.split(__file__)[0], 'Primal')

print (primal_location)

primal = load_physical(primal_location)



#!