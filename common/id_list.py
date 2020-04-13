from random import choice

class id_list(list):
    def __init__(self, name, join='_'):
        self.name = name
        self.join = join

    def __call__(self):
        nid = self.name
        if nid in self:
            nid = self.join.join((nid, choice("ABCDEFHIJKLMNOPQRSTUVWXYZ")))
        while nid in self:
            nid += choice("013456789")
        self.append(nid)
        return nid
