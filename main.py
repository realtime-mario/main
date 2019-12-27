#!/usr/bin/env python3
import wx
from pathlib import Path
import PIL
import PIL.Image
import PIL.ImageDraw
import math
import json
import time

def PilImageToWxBitmap( myPilImage ):
    myWxImage = wx.Image( myPilImage.size[0], myPilImage.size[1] )
    myWxImage.SetData( myPilImage.convert( 'RGB' ).tobytes() )
    return myWxImage.ConvertToBitmap()

def Merge(*dicts):
    result = {}
    for dict in dicts:
        result.update(dict)
    return result

class Tileset:
    def __init__(self, folder):
        self.folder = Path(folder.resolve())
        self.tiles = {}
        for file in self.folder.glob('*.json'):
            self.tiles[json.stem] = [json.load(file), PIL.Image.open(json.with_suffix('.png'))]

class Physics:
    def localpos(self, globalpos):
        if self.parent == None:return globalpos
        else:
            parent = self.parent.globalpos()
            return [globalpos[0] - parent[0], globalpos[1] - parent[1]]
    def globalpos(self, localpos = None):
        if localpos == None:localpos = self.location
        if self.parent == None:return localpos + self.parent.globalpos()
    def setparent(self, newparent):
        globalpos = self.globalpos()
        self.parent = newparent
        self.location = self.localpos(globalpos)

class TileLayer:
    def __init__(self, meta, data, location = [0, 0], velocity = [0, 0], parent = None):
        self.location = localpos(location)
        self.velocity = velocity
        self.parent = parent 
        self.data = []
        for col in data:
            self.data.append([])
            for tile in col:
                if data == -1:self.data[-1].append(None)
                else:self.data[-1].append(Tile(self, metaset[col][1], metaset[col][0].tiles[metaset[col][1]]))
    def draw(self, image, camera):
        minx = camera[0]-int(self.location[0])
        miny = camera[1]-int(self.location[1])
        maxx = camera[0]-int(self.location[0]) + camera[2]
        maxy = camera[1]-int(self.location[1]) + camera[3]
        tileix = math.floor(minx / 16)
        tileiy = math.floor(miny / 16)
        tileax = math.floor(maxx / 16)
        tileay = math.floor(maxy / 16)
        for x in range(tileix, tileax + 1):
            for y in range(tileiy, tileay + 1):
                self.data[x][y].draw(image)

class Tile(TileLayer):
    def __init__(self, name, properties, image, location = [0, 0], velocity = [0, 0], parent = None):
        self.location = localpos(location)
        self.velocity = velocity
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
            width = image.size[0] / properties['frames'])
            empty = data.copy()
            del empty['frames']
            for item in range(properties['frames']):
                full = empty.copy()
                self.frames.append(Frame(full, image.crop((width * item, 0, width * item + width, image.size[1]))))
        else: # one frame
            self.frames.append(Frame(properties, image))
        self.frame = 0
        self.updated = time.time()
                
        
        
class GameRenderer:
    def __init__(self):
        pass
    def drawframe(self):
        #image = PIL.Image.new("RGB", (256, 224), "#ff0000")
        image = PIL.Image.open("./graphics/test/0.png")
        return image
        
class GameWindow(wx.Window):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY, size=(4, 3), style=wx.FULL_REPAINT_ON_RESIZE)

        self.renderer = GameRenderer()
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        
        #dc.SetBrush(wx.Brush(wx.Colour("#ff0000")))
        #dc.DrawRectangle(-1, -1, self.GetClientSize().x + 2, self.GetClientSize().y + 2)

        pilimage = self.renderer.drawframe().resize(self.GetClientSize())
        bitmap = PilImageToWxBitmap(pilimage)

        dc.DrawBitmap(bitmap, 0, 0)
        
class GameFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, wx.ID_ANY, "Super Mario Allstars")

        #self.SetBackgroundColour(wx.BLACK)
        
        panel = wx.Panel(self)
        
        frame = GameWindow(panel)
        
        sizer = wx.BoxSizer()
        sizer.Add(frame, 1, wx.SHAPED | wx.ALIGN_CENTER)
        panel.SetSizer(sizer)
        
if __name__ == "__main__":
    me = Path(__file__).resolve()
    groundtileset = Tileset(Path(me) / Path("../graphics/SMW/grass"))
    
    app = wx.App()
    frame = GameFrame()
    frame.Show()
    app.MainLoop()
