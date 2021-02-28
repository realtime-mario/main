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
import files
import player
import wx.adv
from pydub import AudioSegment

def runmusic(file):
    print(file)
    sound = AudioSegment.from_mp3(src).export(format="wav")
    while True:
        playsound(file)

def convert(file):
    wav = AudioSegment.from_mp3(file).export(format="wav")
    wav.seek(0)
    sound = wx.adv.Sound()
    sound.CreateFromData(wav.read())
    return sound
    
def startsound(sound):
    convert(sound).Play(wx.adv.SOUND_ASYNC)

music = None

def setmusic(sound):
    global music
    if music != None:music.Stop()
    if sound == None:music = None
    else:
        music = convert(sound)
        music.Play(wx.adv.SOUND_ASYNC | wx.adv.SOUND_LOOP)


def PilImageToWxBitmap( myPilImage ):
    myWxImage = wx.Image( myPilImage.size[0], myPilImage.size[1] )
    myWxImage.SetData( myPilImage.convert( 'RGB' ).tobytes() )
    return myWxImage.ConvertToBitmap()

def Merge(*dicts):
    result = {}
    for dict in dicts:
        result.update(dict)
    return result

width = 25
height = 15

class MotionTimer(wx.Timer):
    def __init__(self, frame, sprites, *args, **kw):
        super().__init__(*args, **kw)
        self.frame = frame
        self.sprites = sprites
    def Notify(self):
        i = 0
        while i < len(self.sprites):
            if self.sprites[i].dead:
                if isinstance(self.sprites[i], player.Mario):
                    startlevel(self.sprites[i].world().level)
                else:
                    self.sprites.pop(i)
                    i -= 1
            else:self.sprites[i].move(self.sprites, self.frame.keys, self.frame.events)
            i += 1
        self.frame.Refresh()
        self.frame.events[0] = False
        self.frame.events[1] = False
        self.frame.events[2] = False

class GameRenderer:
    def __init__(self):
        pass
    def drawframe(self, frame):
        size = frame.GetClientSize()
        tile = min(size[0] / width, size[1] / height)
        fixed = (int(tile * width), int(tile * height))
        image = PIL.Image.new("RGB", fixed, "#5c94fc")
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

        self.SetBackgroundColour(wx.BLACK)
        
        panel = wx.Panel(self)
        
        frame = GameWindow(panel, self)
        
        sizer = wx.BoxSizer()
        sizer.Add(frame, 1, wx.SHAPED | wx.ALIGN_CENTER)
        panel.SetSizer(sizer)

        frame.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        frame.Bind(wx.EVT_KEY_UP, self.onKeyUp)

        self.keys = [False, False, False, False, False, False, False, False]
        self.events = [False, False, False]
    def onKeyDown(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:exit()
        elif keycode == wx.WXK_RIGHT:self.keys[0] = True
        elif keycode == wx.WXK_UP:self.keys[1] = True
        elif keycode == wx.WXK_LEFT:self.keys[2] = True
        elif keycode == wx.WXK_DOWN:self.keys[3] = True
        elif keycode == ord('Z'):self.keys[4] = True # run
        elif keycode == ord('X') and not self.keys[5]: # powerup ability
            self.keys[5] = True
            self.events[0] = True
        elif keycode == ord('A') and not self.keys[6]: # jump
            self.keys[6] = True
            self.events[1] = True
        elif keycode == ord('S') and not self.keys[7]: # spin jump
            self.keys[7] = True
            self.events[2] = True
        elif keycode == ord(' '):startlevel('levels/test/1')
        event.Skip()
    def onKeyUp(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RIGHT:self.keys[0] = False
        elif keycode == wx.WXK_UP:self.keys[1] = False
        elif keycode == wx.WXK_LEFT:self.keys[2] = False
        elif keycode == wx.WXK_DOWN:self.keys[3] = False
        elif keycode == ord('Z'):self.keys[4] = False # run
        elif keycode == ord('X'):self.keys[5] = False # powerup ability
        elif keycode == ord('A'):self.keys[6] = False # jump
        elif keycode == ord('S'):self.keys[7] = False # spin jump
        event.Skip()

timer = None
frame = None

def startlevel(file):
    global world, sprites, timer
    world, sprites = files.load(file)
    setmusic('resources/{}.mp3'.format(world.music))
    if timer != None:timer.Stop()
    timer = MotionTimer(frame, sprites)
    timer.Start(17)

if __name__ == "__main__":
    me = Path(__file__).resolve()
    
    app = wx.App()
    frame = GameFrame()
    frame.Show()

    startlevel('levels/test/1')
    
    app.MainLoop()
