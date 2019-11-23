#!/usr/bin/env python3
import tileset
import json
import pygame

pygame.init()
screen = pygame.display.set_mode((512, 512))

clock = pygame.time.Clock()

grass = tileset.tileset('graphics/SMW/grass/', (64, 64))
#                         0                       1               2                   3                4                  5                  6                 7                            8
layer = tileset.layer([(grass, 'middle'), (grass, 'right'), (grass, 'top'), (grass, 'topright'), (grass, 'left'), (grass, 'topleft'), (grass, 'bottom'), (grass, 'bottomright'), (grass, 'bottomleft'),
                       (grass, 'topleftconcave'), (grass, 'toprightconcave'), (grass, 'bottomleftconcave'), (grass, 'bottomrightconcave')],
                      #           9                          10                          11                              12
                      [[-1,-1, 5, 2, 2, 2, 2, 3],
                       [-1,-1, 4, 0, 0, 0, 0, 1],
                       [ 5, 2, 9, 0, 0, 0, 0, 1],
                       [ 8, 6,11, 0, 0, 0, 0, 1],
                       [-1,-1, 8, 6, 6, 6, 6, 7],
                       [ 5, 3,-1,-1,-1,-1,-1,-1],
                       [ 4,10, 2, 2, 2, 2, 2, 3],
                       [ 8, 6, 6, 6, 6, 6, 6, 7]], (64, 64))

chevron = pygame.image.load('graphics/SMW/grass/topright.png').convert_alpha()
big = pygame.transform.scale(chevron, (32, 32))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.fill((255, 255, 255))
    layer.draw(screen, (0, 0))
    pygame.display.flip()
    clock.tick(60)
