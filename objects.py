#!/usr/bin/env python3
class Physics:
    def localpos(self, globalpos):
        parent = self.globalpos()
        return [globalpos[0] - parent[0], globalpos[1] - parent[1]]
    def globalpos(self, localpos = None):
        if localpos == None:localpos = [0, 0]
        return localpos + self.parent.globalpos() 
    def globalvelocity(self):
        return self.velocity + self.parent.globalvelocity()
    def setparent(self, newparent):
        globalpos = self.globalpos()
        self.parent = newparent
        self.location = self.localpos(globalpos)
    def move(self, sprites):pass
    def draw(self, image, camera):pass

class World(Physics):
    def localpos(self, globalpos):
        return globalpos
    def globalpos(self, localpos = None):
        if localpos == None:return [0, 0]
        return localpos
    def globalvelocity(self):return [0, 0]
    def setparent(self, newparent):
        raise TypeError('The world cannot have a parent.')
