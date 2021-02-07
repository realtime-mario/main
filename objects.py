#!/usr/bin/env python3
class Physics:
    def localpos(self, globalpos):
        parent = self.globalpos()
        return [globalpos[0] - parent[0], globalpos[1] - parent[1]]
    def globalpos(self, localpos = None):
        if localpos == None:localpos = [0, 0]
        return self.parent.globalpos([localpos[0] + self.location[0], localpos[1] + self.location[1]])
    def globalvelocity(self):
        return self.velocity + self.parent.globalvelocity()
    def setparent(self, newparent):
        globalpos = self.globalpos()
        self.parent = newparent
        self.location = self.localpos(globalpos)
    def move(self, sprites):pass
    def draw(self, image, camera):pass
    def collide(self, left, top, width, height):return [None, None, None, None]

class World(Physics):
    def localpos(self, globalpos):
        return globalpos
    def globalpos(self, localpos = None):
        if localpos == None:return [0, 0]
        return localpos
    def globalvelocity(self):return [0, 0]
    def setparent(self, newparent):
        raise TypeError('The world cannot have a parent.')
