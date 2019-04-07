#!/usr/bin/env python
import cairo
import pygame
import math
import rsvg

pygame.init()

def fixed_svg(svg, size):
    try:handle = rsvg.Handle(svg)
    except TypeError:handle = svg
    original_size = (
        handle.props.width,
        handle.props.height
    )
    scale = size[0]/float(original_size[0]), size[1]/float(original_size[1])
    return scale_svg(handle, scale, size)
def scale_svg(svg, scale, size=None):
    try:handle = rsvg.Handle(svg)
    except TypeError:handle = svg

    if size == None:
        size = (
            handle.props.width,
            handle.props.height
        )
    
    page = pygame.Surface(size).convert_alpha()
    page.fill((0, 0, 0, 0))

    pixels = pygame.surfarray.pixels2d(page)

    cairo_surface = cairo.ImageSurface.create_for_data(
        pixels.data, cairo.FORMAT_ARGB32, size[0], size[1])

    context = cairo.Context(cairo_surface)
    
    context.scale(scale[0], scale[1])

    handle.render_cairo(context)
    
    return page
