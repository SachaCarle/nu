import sys, os, subprocess

def moved(entity, destination, **pray):
    old = os.path.split(entity.location)[0]
    entity.think('I will ask father to move me.', old, destination)
    entity.pray("move", old, str(destination), **pray)
    entity.think('I will sleep now...')
    exit()
