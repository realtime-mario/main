#!/usr/bin/env python3
import wx
from pathlib import Path
import PIL
import PIL.Image

def PilImageToWxBitmap( myPilImage ):
    myWxImage = wx.Image( myPilImage.size[0], myPilImage.size[1] )
    myWxImage.SetData( myPilImage.convert( 'RGB' ).tobytes() )
    return myWxImage.ConvertToBitmap()

class Tileset:
    def __init__(self, folder):
        self.folder = Path(folder.resolve())

class GameRenderer:
    def __init__(self):
        pass
    def drawframe(self):
        image = PIL.Image.new("RGB", (256, 224), "#ff0000")
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
