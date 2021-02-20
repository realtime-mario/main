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
        self.possiblegravity = [[0.02734375 , 0.0078125    ],
                                [0.0234375  , 0.00732421875],
                                [0.03515625 , 0.009765625  ],
                                [0.009765625, 0.009765625  ]]
        self.gravity = 3
        self.acceleration = [0.0023193359375, 0.00347900390625]
        self.deceleration = [0.00634765625, 0.00634765625]
        self.friction = [0.003173828125, 0.003173828125]
        self.maxspeed = [0.09765625, 0.16015625]
        self.possiblejump = [0.25, 0.25, 0.3125]
        self.dead = False
        for i in range(len(animations)):
            self.images.append(PIL.Image.open('resources/{}/{}/{}.png'.format(self.path, powerups[self.powerup], animations[i])))
    def jumprange(self):
        speed = abs(self.globalvelocity()[0])
        if speed < 0.0625:return 0
        elif speed < 0.1445159912109375:return 1
        else:return 2
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
    def move(self, sprites, keys, events):
        self.velocity[1] += self.possiblegravity[self.gravity][keys[6]]
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
                if events[1]:
                    self.gravity = self.jumprange()
                    self.velocity[1] -= self.possiblejump[self.gravity]
                else:
                    self.gravity = 3
            else:
                self.location[1] += velocity[1]

        if self.globalpos()[1] > 15:self.dead = True

        direction = 0

        if keys[0]:direction += 1
        if keys[2]:direction -= 1

        if direction == 0:
            if abs(self.velocity[0]) < self.friction[keys[5]]:self.velocity[0] = 0
            elif self.velocity[0] > 0:self.velocity[0] -= self.friction[keys[5]]
            else:self.velocity[0] += self.friction[keys[5]]
        elif direction > 0:
            if self.velocity[0] > 0:
                self.velocity[0] += self.acceleration[keys[5]]
                if self.velocity[0] > self.maxspeed[keys[5]]:self.velocity[0] = self.maxspeed[keys[5]]
            else:self.velocity[0] += self.deceleration[keys[5]]
        else:
            if self.velocity[0] < 0:
                self.velocity[0] -= self.acceleration[keys[5]]
                if -self.velocity[0] > self.maxspeed[keys[5]]:self.velocity[0] = -self.maxspeed[keys[5]]
            else:self.velocity[0] -= self.deceleration[keys[5]]
