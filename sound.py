#!/usr/bin/env python3
import wx
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
