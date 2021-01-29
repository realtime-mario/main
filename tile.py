#!/usr/bin/env python3
import objects
import json
from pathlib import Path
import PIL
import PIL.Image
import PIL.ImageDraw
import math
import time

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

#class Tileset:
#    def __init__(self, folder):
#        self.folder = Path(folder.resolve())
#        self.tiles = {}
#        for file in self.folder.glob('*.json'):
#            with open(file) as f:data = json.load(f)
#            self.tiles[file.stem] = [data, PIL.Image.open(file.with_suffix('.png'))]

class TileLayer(objects.Physics):
    def __init__(self, metaset, data, location = [0, 0], parent = None):
        data = rotate(data)
        self.parent = parent
        self.location = self.localpos(location)
        self.data = []
        for col in range(len(data)):
            self.data.append([])
            for tile in range(len(data[col])):
                if data[col][tile] == -1:self.data[-1].append(None)
                else:
                    name = metaset[data[col][tile]]
                    with open('resources/{}.json'.format(name)) as f:
                        properties = json.load(f)
                    image = PIL.Image.open('resources/{}.png'.format(name))
                    self.data[-1].append(Tile(name, properties, image, [tile, col]))
    def draw(self, image, camera):
        minx = camera[0]-int(self.location[0])
        miny = camera[1]-int(self.location[1])
        maxx = camera[0]-int(self.location[0]) + int(camera[2] / camera[4])
        maxy = camera[1]-int(self.location[1]) + int(camera[3] / camera[4])
        tileix = max((minx), 0)
        tileiy = max((miny), 0)
        tileax = min((maxx), len(self.data[0])-1)
        tileay = min((maxy), len(self.data)-1)
        for x in range(tileix, tileax + 1):
            for y in range(tileiy, tileay + 1):
                tile = self.data[y][x]
                if tile != None:
                    tile.draw(image, camera)

class Tile(TileLayer):
    def __init__(self, name, properties, image, location = [0, 0], parent = None):
        self.parent = parent
        self.location = self.localpos(location)
        self.parent = parent
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
        minx = camera[0]-int(self.location[0])
        miny = camera[1]-int(self.location[1])
        maxx = camera[0]-int(self.location[0]) + camera[2]
        maxy = camera[1]-int(self.location[1]) + camera[3]
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
