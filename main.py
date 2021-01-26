#!/usr/bin/env python3
import wx
from pathlib import Path
import PIL
import PIL.Image
import PIL.ImageDraw
import math
import json
import time

def rotate(list):
    result = [[None] * len(list) for i in range(len(list[0]))]
    for i in range(len(list)):
        for j in range(len(list[0])):
            result[j][i] = list[i][j]
    result.reverse()
    return result

def PilImageToWxBitmap( myPilImage ):
    myWxImage = wx.Image( myPilImage.size[0], myPilImage.size[1] )
    myWxImage.SetData( myPilImage.convert( 'RGB' ).tobytes() )
    return myWxImage.ConvertToBitmap()

def Merge(*dicts):
    result = {}
    for dict in dicts:
        result.update(dict)
    return result

class Frame:
    def __init__(self, properties, image):
        self.image = image

class Tileset:
    def __init__(self, folder):
        self.folder = Path(folder.resolve())
        self.tiles = {}
        for file in self.folder.glob('*.json'):
            with open(file) as f:data = json.load(f)
            self.tiles[file.stem] = [data, PIL.Image.open(file.with_suffix('.png'))]

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

class TileLayer(Physics):
    def __init__(self, metaset, data, location = [0, 0], velocity = [0, 0], parent = None):
        data = rotate(data)
        self.parent = parent
        self.location = self.localpos(location)
        self.velocity = velocity
        self.data = []
        for col in range(len(data)):
            self.data.append([])
            for tile in range(len(data[col])):
                if data[col][tile] == -1:self.data[-1].append(None)
                else:
                    name = metaset[data[col][tile]]
                    with open('graphics/{}.json'.format(name)) as f:
                        properties = json.load(f)
                    image = PIL.Image.open('graphics/{}.png'.format(name))
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
    def __init__(self, name, properties, image, location = [0, 0], velocity = [0, 0], parent = None):
        self.parent = parent
        self.location = self.localpos(location)
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


display = TileLayer(['SMW/overworld/topleft', 'SMW/overworld/left', 'SMW/overworld/top', 'SMW/overworld/middle', 'SMW/overworld/right', 'SMW/overworld/topright', 'SMW/overworld/bottomrightconcave', 'SMW/overworld/bottomleftconcave'],
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
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [ 3, 2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
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
                     ])

width = 25
height = 15

class GameRenderer:
    def __init__(self):
        pass
    def drawframe(self, frame):
        size = frame.GetClientSize()
        tile = min(size[0] / width, size[1] / height)
        fixed = (int(tile * width), int(tile * height))
        image = PIL.Image.new("RGB", fixed, "#ff0000")
        display.draw(image, (0, 0, fixed[0], fixed[1], tile))
        #image = PIL.Image.open("./graphics/test/0.png")
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
    groundtileset = Tileset(Path(me) / Path("../graphics/SMW/grass"))
    
    app = wx.App()
    frame = GameFrame()
    frame.Show()
    app.MainLoop()
