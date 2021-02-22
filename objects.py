#!/usr/bin/env python3
from pathlib import Path
import PIL
import PIL.Image
import time
class Physics:
    def __init__(self):
        self.dead = False
    def localpos(self, globalpos):
        parent = self.globalpos()
        return [globalpos[0] - parent[0], globalpos[1] - parent[1]]
    def globalpos(self, localpos = None):
        if localpos == None:localpos = [0, 0]
        return self.parent.globalpos([localpos[0] + self.location[0], localpos[1] + self.location[1]])
    def globalvelocity(self):
        parent = self.parent.globalvelocity()
        return [self.velocity[0] + parent[0], self.velocity[1] + parent[1]]
    def setparent(self, newparent):
        globalpos = self.globalpos()
        self.parent = newparent
        self.location = self.localpos(globalpos)
    def move(self, sprites, keys, events):pass
    def draw(self, image, camera):pass
    def collide(self, left, top, width, height):return [None, None, None, None]
    def world(self):return self.parent.world()

class World(Physics):
    def __init__(self, level):
        self.level = level
        self.dead = False
    def localpos(self, globalpos):
        return globalpos
    def globalpos(self, localpos = None):
        if localpos == None:return [0, 0]
        return localpos
    def globalvelocity(self):return [0, 0]
    def setparent(self, newparent):
        raise TypeError('The world cannot have a parent.')
    def world(self):return self

loaded = 0

def openimage(file):
    global loaded
    image = PIL.Image.open(file)
    copy = image.copy()
    image.close()
    loaded += 1
    print('({}) loading {}'.format(loaded, file))
    return copy

class Animation:
    def __init__(self, location):
        if Path(location + '.png').is_file():
            self.delay = 1000
            self.images = [openimage(location + '.png')]
        else:
            with open(location + '.txt') as f:self.delay = int(f.read())
            self.images = []
            i = 1
            while True:
                file = '{}{}.png'.format(location, i)
                if Path(file).is_file():self.images.append(openimage(file))
                else:break
                i += 1
    def image(self):
        miliseconds = time.time() * 1000
        frame = int(miliseconds // self.delay)
        return self.images[frame % len(self.images)]
