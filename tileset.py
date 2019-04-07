#!/usr/bin/env python
import pygame
import time
import os
import json

def crop(image, size):
    new = pygame.Surface(size[2:])
    new.blit(image, (0, 0), size)
    return new

class frame:
    def __init__(self, image, properties, scale):
        self.properties = properties
        self.raw_image = image
        self.image = pygame.transform.scale(image, scale)
        if 'delay' in properties:self.delay = 1000
        else:self.delay = properties['delay']
    def fix_scale(self):
        self.image = pygame.transform.scale(raw_image, scale)
        
class tile:
    def __init__(self, image, properties, scale):
        self.frames = []
        index = 0
        height = image.get_height()
        if 'width' in properties:width = properties['width']
        else:width = height
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
        self.frame = 0
        self.lasttime = time.time()
        self.scale = scale
    def update(self):
        if self.scale != self.frames[self.frame].scale:
            for frame in self.frames:
                frame.scale = self.scale
                frame.fix_scale()
        while self.lasttime + self.frames[self.frame].delay > time.time():
            self.lasttime += self.frames[self.frame].delay
            self.frame += 1
    def draw(self, screen, dest):
        self.update()
        screen.blit(self.frames[self.frame].image, dest)
        
class tileset:
    def __init__(self, directory, scale):
        tiles = 0
        
        files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(directory, f))]
        for name in files:
            if name.split('.')[-1] == 'json':
                tiles += 1
        self.tiles = []
        for index in range(tiles):
            properties = json.load(os.path.join(directory, index + '.json'))
            image = pygame.image.load(os.path.join(directory, index + '.png'))
            self.tiles.append(tile(image, properties, scale))
