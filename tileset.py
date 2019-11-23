import pygame
import time
import os
import json
import gameobjects

def crop(image, size):
    new = pygame.Surface(size[2:]).convert_alpha()
    new.fill((0, 0, 0, 0))
    new.blit(image, (0, 0), size)
    return new

class frame:
    def __init__(self, image, properties, scale):
        self.properties = properties
        self.raw_image = image
        self.image = pygame.transform.scale(image, scale)
        if 'delay' in properties:self.delay = properties['delay'] / 1000
        else:self.delay = 1
        self.scale = scale
    def fix_scale(self):
        self.image = pygame.transform.scale(self.raw_image, self.scale)

class layer(gameobjects.sprite):
    def __init__(self, tiles, contents, scale = (16, 16), parent = None, children = []):
        self.tiles = tiles
        self.contents = contents
        self.setParent(parent)
        self.children = children
        for child in self.children:
            child.setParent(self)
        self.scale = scale
    def tiledata(self, pos):
        x, y = pos
        index = self.contents[y][x] # makes json more natural
        if index == -1:return None
        data = self.tiles[index] # tileset, tilename
        return data[0].tiles[data[1]]
    def draw(self, surface, pos):
        for x in range(len(self.contents)):
            for y in range(len(self.contents[x])):
                tile = self.tiledata((x, y))
                if tile != None:
                    tile.draw(surface, (pos[0] + x * self.scale[0], pos[1] + y * self.scale[1]))
        
class tile(layer):
    def __init__(self, image, properties, scale):
        self.tileset = None
        self.frames = []
        index = 0
        height = image.get_height()
        if 'width' in properties:width = properties['width']
        else:width = height
        if 'per-frame' in properties:
            for group in properties['per-frame']:
                for property in properties:
                    if not property in group:
                        group[property] = properties[property]
                self.frames.append(
                    frame(
                        crop(
                            image,
                            (index*width, 0, width, height)
                        ),
                        group,
                        scale
                    )
                )
                index += 1
        elif 'frames' in properties:
            for i in range(properties['frames']):
                self.frames.append(
                    frame(
                        crop(
                            image,
                            (i*width, 0, width, height)
                        ),
                        properties,
                        scale
                    )
                )
        self.fulldelay = sum(x.delay for x in self.frames)
        print(self.fulldelay, self.frames[0].delay)
        self.frame = 0
        self.lasttime = time.time()
        self.scale = scale
    def tiledata(self, pos):
        if pos[0] == 0 and pos[1] == 0:return self
    def update(self):
        if self.frame >= len(self.frames):self.frame %= len(self.frames)
        if self.scale != self.frames[self.frame].scale:
            for frame in self.frames:
                frame.scale = self.scale
                frame.fix_scale()
        while self.lasttime < time.time():
            now = time.time()
            self.lasttime = ((self.lasttime - now) % self.fulldelay) + now
            print('frame', self.frame, time.time(), self.lasttime)
            self.lasttime += self.frames[self.frame].delay
            self.frame += 1
            if self.frame >= len(self.frames):self.frame %= len(self.frames)
    def draw(self, screen, dest):
        self.update()
        screen.blit(self.frames[self.frame].image, dest)
class tileset:
    def __init__(self, directory, scale = (16, 16)):
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        self.tiles = {}
        for name in files:
            print('file:', name) 
            if name.split('.')[-1] == 'json':
                print(name, 'is a json.')
                json_file = open(os.path.join(directory, name), 'r')
                properties = json.load(json_file)
                json_file.close()
                image = pygame.image.load(os.path.join(directory, name)[0:-5] + '.png').convert_alpha()
                self.image= image # tests
                self.tiles[name[0:-5]] = tile(image, properties, scale)
                self.tiles[name[0:-5]].tileset = self

        
