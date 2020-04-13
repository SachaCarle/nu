from common import NuObject
from random import choice

class DNA(NuObject):

    def __call__(self, key=None):
        return self.dnas[key]

    def __init__(self, entity, *parents, dna={}, state='physical'):
        NuObject.__init__(self)
        self.parents = parents
        self.chart = ""
        self.dnas = {}
        if len(parents) > 0:
            if len(parents) == 1:
                self.auto_reproduction(parents[0])
        else:
            for k,v in dna.items():
                self.dnas[k] = v

    def mutate(self, key, value, *more):
        return value

    def auto_reproduction(self, this):
        self.mutation = False
        self.chart = this.chart
        if choice(range(this.dnas['stability'])) == 0:
            self.chart = this.chart + choice('AZERTYUIOPQSDFGHJKLMWXCVBN')
            self.mutation = True
        for k,v in this.dnas.items():
            self.dnas[k] = self.mutate(k, v)
        #input()











#!