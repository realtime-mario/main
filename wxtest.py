#!/usr/bin/env python3
import wx
import wxtile
class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, -1, 'Super Mario All Stars + Super Mario World')
        self.tileset = wxtile.Tileset('graphics/SMW/grass/')
        self.image = wxtile.Layer(self, -1, [(self.tileset, 'topleft'), (self.tileset, 'top'), (self.tileset, 'topright'),
                                             (self.tileset, 'left'), (self.tileset, 'middle'), (self.tileset, 'right'), 
                                             (self.tileset, 'bottomleft'), (self.tileset, 'bottom'), (self.tileset, 'bottomright')],
                                  [[-1,-1,-1],
                                   [-1,-1,-1],
                                   [ 0, 3, 6]])
        self.image.Show()
        player = wxobjects.Player(self, -1, (12, 0), (8, 10), None)
        

if __name__ == '__main__':
    app = wx.App()

    frame = MainFrame()
    frame.Show()

    app.MainLoop()
