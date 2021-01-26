#!/usr/bin/env python3
class Physics:
    def localpos(self, globalpos):
        if self.parent == None:return globalpos
        else:
            parent = self.parent.globalpos()
            return [globalpos[0] - parent[0], globalpos[1] - parent[1]]
    def globalpos(self, localpos = None):
        if localpos == None:localpos = self.location
        if self.parent == None:return localpos + self.parent.globalpos()
    def setparent(self, newparent):
        globalpos = self.globalpos()
        self.parent = newparent
        self.location = self.localpos(globalpos)
