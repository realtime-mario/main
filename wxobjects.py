#!/usr/bin/env python3
import wx
import wxtile
class Physics(wx.Panel):
    def __init__(self, parent, id, pos, size):
        super().__init__(parent, id)
        self.SetPosition(pos)
        self.SetSize(size)
        self.velocity = [0, 0]
        self.collides = set()
    def Collide(self, other):return False
    def Compare(self, other):
        if self.getPosition().x + self.getSize().width < other.getPosition().x:return False
        if other.getPosition().x + other.getSize().width < self.getPosition().x:return False
        if self.getPosition().y + self.getSize().height < other.getPosition().y:return False
        if other.getPosition().y + other.getSize().height < self.getPosition().y:return False
        if not self.Collide(other):return other.Collide(self)
        return True
class Player(Physics):
    def __init__(self, parent, id, pos, size, image):
        super().__init__(parent, id, pos, size)
        self.image = image
        self.collides = {wxtile.Tile}
