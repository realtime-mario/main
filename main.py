#!/usr/bin/env python3
import wx
from pathlib import Path
import PIL
import PIL.Image
import PIL.ImageDraw
import math

def PilImageToWxBitmap( myPilImage ):
    myWxImage = wx.Image( myPilImage.size[0], myPilImage.size[1] )
    myWxImage.SetData( myPilImage.convert( 'RGB' ).tobytes() )
    return myWxImage.ConvertToBitmap()

class Tileset:
    def __init__(self, folder):
        self.folder = Path(folder.resolve())
        self.tiles = {}
        for json in self.folder.glob('*.json'):
            self.tiles[json.stem] = PIL.Image.open(json.with_suffix('.png'))

class TileLayer:
    def __init__(self, meta, data):
        self.location = [0, 0]
        self.velocity = [0, 0]
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
