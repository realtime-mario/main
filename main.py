#!/usr/bin/env python3
import wx
from pathlib import Path
import PIL
import PIL.Image
import PIL.ImageDraw
import math
import json
import time
import objects
import tile
import player

def PilImageToWxBitmap( myPilImage ):
    myWxImage = wx.Image( myPilImage.size[0], myPilImage.size[1] )
    myWxImage.SetData( myPilImage.convert( 'RGB' ).tobytes() )
    return myWxImage.ConvertToBitmap()

def Merge(*dicts):
    result = {}
    for dict in dicts:
        result.update(dict)
    return result

world = objects.World()

sprites = []

sprites.append(tile.TileLayer(world, ['SMW/overworld/topleft', 'SMW/overworld/left', 'SMW/overworld/top', 'SMW/overworld/middle', 'SMW/overworld/right', 'SMW/overworld/topright', 'SMW/overworld/bottomrightconcave', 'SMW/overworld/bottomleftconcave'],
                    [[ 1, 0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 4, 5,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 1, 0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 6, 1, 1, 1, 0,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 3, 3, 3, 3, 6, 0,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 7, 4, 4, 4, 4, 5,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 4, 5,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     ]))

sprites.append(player.Mario(world, [2, 2]))

width = 25
height = 15

class MotionTimer(wx.Timer):
    def __init__(self, frame, sprites, *args, **kw):
        super().__init__(*args, **kw)
        self.frame = frame
        self.sprites = sprites
    def Notify(self):
        for sprite in self.sprites:
            sprite.move(self.sprites)
        self.frame.Refresh()

class GameRenderer:
    def __init__(self):
        pass
    def drawframe(self, frame):
        size = frame.GetClientSize()
        tile = min(size[0] / width, size[1] / height)
        fixed = (int(tile * width), int(tile * height))
        image = PIL.Image.new("RGB", fixed, "#ff0000")
        camera = 0, 0, fixed[0], fixed[1], tile
        for display in sprites:
            display.draw(image, camera)
        return image
        
class GameWindow(wx.Window):
    def __init__(self, parent, frame):
        super().__init__(parent, wx.ID_ANY, size=(width, height), style=wx.FULL_REPAINT_ON_RESIZE)

        self.renderer = GameRenderer()

        self.frame = frame
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        
        #dc.SetBrush(wx.Brush(wx.Colour("#ff0000")))
        #dc.DrawRectangle(-1, -1, self.GetClientSize().x + 2, self.GetClientSize().y + 2)

        pilimage = self.renderer.drawframe(frame).resize(self.GetClientSize())
        bitmap = PilImageToWxBitmap(pilimage)

        dc.DrawBitmap(bitmap, 0, 0)
        
class GameFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, wx.ID_ANY, "Super Mario All-Stars")

        #self.SetBackgroundColour(wx.BLACK)
        
        panel = wx.Panel(self)
        
        frame = GameWindow(panel, self)
        
        sizer = wx.BoxSizer()
        sizer.Add(frame, 1, wx.SHAPED | wx.ALIGN_CENTER)
        panel.SetSizer(sizer)
        
if __name__ == "__main__":
    me = Path(__file__).resolve()
    
    app = wx.App()
    frame = GameFrame()
    frame.Show()

    timer = MotionTimer(frame, sprites)
    timer.Start(33)
    
    app.MainLoop()
