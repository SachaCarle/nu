from entity import Entity
from pathlib import Path

@Entity()
def lol(*args, **kwargs):
    print ('Hello World, ', args, kwargs)

e = Entity(
    mind = (Path('../comon.py'), Path('../head.py')),
)


print (lol)
#!