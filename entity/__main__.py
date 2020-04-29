from entity import Entity
from pathlib import Path

@Entity(mind=f"""
print ('What that ?')
""")
def lol(self, this):
    print ('Hello World, ', this)



e = Entity(mind = Path('common.py'))
e.think('lolz')

@Entity(mind = Path('common.py'))
def exemple(self, this):
    self.me.think('Lolz')


e = Entity(mind = Path('common.py'), main = Path('main.py'))
e('main')

#!