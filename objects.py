#!/usr/bin/env python3
class Physics:
    def localpos(self, globalpos):
        if self.parent == None:return globalpos
        else:
            parent = self.globalpos()
            return [globalpos[0] - parent[0], globalpos[1] - parent[1]]
    def globalpos(self, localpos = None):
        if localpos == None:localpos = [0, 0]
        if self.parent == None:return localpos
        else:return localpos + self.parent.globalpos() 
    def globalvelocity(self):
        if self.parent == None:return self.velocity
        return self.velocity + self.parent.globalvelocity()
    def setparent(self, newparent):
        globalpos = self.globalpos()
        self.parent = newparent
        self.location = self.localpos(globalpos)
    def move(self, sprites):pass
    def draw(self, image, camera):pass
