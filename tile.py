#!/usr/bin/env python3
import objects
import json
from pathlib import Path
import PIL
import PIL.Image
import PIL.ImageDraw
import math
import time

def tint_image(im, color):
    color_map = []
    for component in color:
        color_map.extend(int(component/255.0*i) for i in range(256))
    return im.point(color_map)

def rotate(list):
    result = [[None] * len(list) for i in range(len(list[0]))]
    for i in range(len(list)):
        for j in range(len(list[0])):
            result[j][i] = list[i][j]
    result.reverse()
    return result

class Frame:
    def __init__(self, properties, image):
        self.image = image
        self.properties = properties

class TileLayer(objects.Physics):
    def __init__(self, parent, metaset, data, location = [0, 0]):
        self.dead = False
        data = rotate(data)
        self.parent = parent
        self.location = self.parent.localpos(location)
        self.data = []
        for col in range(len(data)):
            self.data.append([])
            for tile in range(len(data[col])):
                if data[col][tile] == -1:self.data[-1].append(None)
                else:
                    name = metaset[data[col][tile]]
                    with open('resources/{}.json'.format(name)) as f:
                        properties = json.load(f)
                    image = objects.openimage('resources/{}.png'.format(name))
                    self.data[-1].append(Tile(self, name, properties, image, [tile, col]))
    def draw(self, image, camera):
        minx, miny = self.localpos(camera[0:2])
        maxx, maxy = self.localpos((camera[0] + int(camera[2] / camera[4]), camera[1] + int(camera[3] / camera[4])))
        tileix = max((minx), 0)
        tileiy = max((miny), 0)
        tileax = min((maxx), len(self.data[0])-1)
        tileay = min((maxy), len(self.data)-1)
        for x in range(tileix, tileax + 1):
            for y in range(tileiy, tileay + 1):
                tile = self.data[y][x]
                if tile != None:
                    tile.draw(image, camera)
    def collide(self, left, top, width, height):
        minx, miny = self.localpos((left, top))
        #print(left,top, width, height)
        maxx, maxy = self.localpos((left + width, top + height))
        tileix = math.floor(max(minx - 1, 0))
        tileiy = math.floor(max(miny - 1, 0))
        tileax = math.ceil(min(maxx + 1, len(self.data[0])-1))
        tileay = math.ceil(min(maxy + 1, len(self.data)-1))
        result = [None, None, None, None]
        #print('start', tileix, tileax, tileiy, tileay)
        for x in range(tileix, tileax + 1):
            for y in range(tileiy, tileay + 1):
                tile = self.data[y][x]
                #print(x, y, tile)
                if tile != None:
                    next = tile.collide(left, top, width, height)
                    for i in range(4):
                        if next[i] != None and (result[i] == None or result[i] > next[i]):result[i] = next[i]
        return result

class Tile(TileLayer):
    def __init__(self, parent, name, properties, image, location = [0, 0]):
        self.dead = False
        self.parent = parent
        self.location = self.parent.localpos(location)
        self.frames = []
        if 'per-frame' in properties:
            width = image.size[0] / len(properties['per-frame'])
            empty = data.copy()
            del empty['per-frame']
            for item in range(len(properties['per-frame'])):
                full = Merge(properties['per-frame'][item], empty)
                self.frames.append(Frame(full, image.crop((width * item, 0, width * item + width, image.size[1]))))
        elif 'frames' in properties:
            width = image.size[0] / properties['frames']
            empty = properties.copy()
            del empty['frames']
            for item in range(properties['frames']):
                full = empty.copy()
                self.frames.append(Frame(full, image.crop((width * item, 0, width * item + width, image.size[1]))))
        else: # one frame
            self.frames.append(Frame(properties, image))
        if 'delay' in properties:
            self.delay = properties['delay'] / 1000
        else:
            self.delay = 1
    def draw(self, image, camera):
        size = math.ceil(camera[4])
        minx, miny = self.localpos(camera[0:2])
        maxx, maxy = self.localpos((camera[0] + camera[2], camera[1] + camera[3]))
        frame = self.frames[int(time.time() / self.delay) % len(self.frames)]
        scaled = frame.image.resize((size, size), PIL.Image.NEAREST)
        try:
            image.paste(scaled,
                        (int(-camera[0] + camera[4] * self.location[0]),
                         int(-camera[1] + camera[4] * self.location[1])),
                        scaled) # First is colour. Last is transparency. Default is full opacity everywhere.
        except ValueError:
            image.paste(scaled,
                        (int(-camera[0] + camera[4] * self.location[0]),
                         int(-camera[1] + camera[4] * self.location[1])))
    def collide(self, left, top, width, height):
        solidity = self.frames[int(time.time() / self.delay) % len(self.frames)].properties.get('solidity', 0)
        minx, miny = self.localpos((left, top))
        maxx, maxy = self.localpos((left + width, top + height))
        result = [None, None, None, None]
        if solidity & 4 and maxx <= 0 and maxy > 0 and miny < 1:result[0] = -maxx
        if solidity & 2 and maxy <= 0 and maxx > 0 and minx < 1:result[1] = -maxy
        if solidity & 1 and minx >= 1 and maxy > 0 and miny < 1:result[2] = minx - 1
        if solidity & 8 and miny >= 1 and maxx > 0 and minx < 1:result[3] = miny - 1
        return result
        
