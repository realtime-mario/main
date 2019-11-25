#!/usr/bin/env python3
import wx
import wxtile
class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, -1, 'Super Mario All Stars + Super Mario World')
        self.image = wxtile.Layer(self, -1, [], [[0, 0], [0, 0]])
        self.image.Show()
        

if __name__ == '__main__':
    app = wx.App()

    frame = MainFrame()
    frame.Show()

    app.MainLoop()
