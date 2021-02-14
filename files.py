#!/usr/bin/env python3
import json
import objects
import tile
import player
version = [0, 1, 0]
def load(file):
    with open(file) as f:data = json.load(f)
    if data['version'][0] != version[0] or data['version'][1] > version[1]:
        print('This level was made for {}. You are currently playing on version {}.'.format(
            '.'.join(data['version']), '.'.join(version)))
    
    world = objects.World()
    sprites = []
    for sprite in data['sprites']:
        if sprite['type'] == 'tilelayer':
            sprites.append(tile.TileLayer(world, sprite['tileset'], sprite['map']))
        else:
            raise TypeError('Cannot load {} referenced in {}. Unknown object type.'.format(sprite['type'], file))
    sprites.append(player.Mario(world, data['mariostart']))
    return world, sprites
