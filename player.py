#!/usr/bin/env python3
import objects
from pathlib import Path
import PIL
import PIL.Image
import math

powerups = 'small', 'big', 'fire',
animations = 'idle',

def negate(list):
    return [-x for x in list]

class Mario(objects.Physics):
    def __init__(self, parent, globalpos, powerup = 0, path = 'SMW/global/mario', velocity = [0, 0]):
        self.parent = parent
        self.path = path
        self.location = self.parent.localpos(globalpos)
        self.powerup = powerup
        self.velocity = velocity
        self.animation = 0
        self.images = []
        self.right = True
        self.gravity = 0.03
        self.acceleration = 0.005
        self.deceleration = 0.03
        self.friction = 0.005
        self.maxspeed = 0.5
        self.jump = 0.7
        self.dead = False
        for i in range(len(animations)):
            self.images.append(PIL.Image.open('resources/{}/{}/{}.png'.format(self.path, powerups[self.powerup], animations[i])))
    def draw(self, image, camera):
        size = math.ceil(camera[4] * 2)
        minx = camera[0]-int(self.location[0])
        miny = camera[1]-int(self.location[1])
        maxx = camera[0]-int(self.location[0]) + camera[2]
        maxy = camera[1]-int(self.location[1]) + camera[3]
        scaled = self.images[self.animation].resize((size, size), PIL.Image.NEAREST)
        if self.right:
            scaled = scaled.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        try:
            image.paste(scaled,
                        (int(-camera[0] + camera[4] * (self.location[0] - 1)),
                         int(-camera[1] + camera[4] * (self.location[1] - 2))),
                        scaled) # First is colour. Last is transparency. Default is full opacity everywhere.
        except ValueError:
            image.paste(scaled,
                        (int(-camera[0] + camera[4] * (self.location[0] - 1)),
                         int(-camera[1] + camera[4] * (self.location[1] - 2))))
    def move(self, sprites, keys):
        self.velocity[1] += self.gravity
        collision = [None, None, None, None]
        for sprite in sprites:
            next = sprite.collide(self.globalpos()[0] - 0.5, self.globalpos()[1] - 1, 1, 1)
            for i in range(4):
                if next[i] != None and (collision[i] == None or collision[i] > next[i]):collision[i] = next[i]

        velocity = self.globalvelocity()
        if velocity[0] > 0:
            if collision[0] != None and velocity[0] > collision[0]:
                self.velocity[0] = -self.parent.globalvelocity()[0]
                self.location[0] += collision[0]
            else:
                self.location[0] += velocity[0]
        elif velocity[0] < 0:
            if collision[2] != None and -velocity[0] > collision[2]:
                self.velocity[0] = -self.parent.globalvelocity()[0]
                self.location[0] -= collision[2]
            else:
                self.location[0] += velocity[0]
        if velocity[1] < 0:
            if collision[3] != None and -velocity[1] > collision[3]:
                self.velocity[1] = -self.parent.globalvelocity()[1]
                self.location[1] -= collision[3]
            else:
                self.location[1] += velocity[1]
        elif velocity[1] > 0:
            if collision[1] != None and velocity[1] > collision[1]:
                self.velocity[1] = -self.parent.globalvelocity()[1]
                self.location[1] += collision[1]
                if keys[6]:self.velocity[1] -= self.jump
            else:
                self.location[1] += velocity[1]

        if self.globalpos()[1] > 15:self.dead = True

        direction = 0

        if keys[0]:direction += 1
        if keys[2]:direction -= 1

        if direction == 0:
            if abs(self.velocity[0]) < self.friction:self.velocity[0] = 0
            elif self.velocity[0] > 0:self.velocity[0] -= self.friction
            else:self.velocity[0] += self.friction
        elif direction > 0:
            if self.velocity[0] > 0:
                self.velocity[0] += self.acceleration
                if self.velocity[0] > self.maxspeed:self.velocity[0] = self.maxspeed
            else:self.velocity[0] += self.deceleration
        else:
            if self.velocity[0] < 0:
                self.velocity[0] -= self.acceleration
                if -self.velocity[0] > self.maxspeed:self.velocity[0] = -self.maxspeed
            else:self.velocity[0] -= self.deceleration
