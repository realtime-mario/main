import wx
import json
import os
import wxobjects

class Tileset:
    def __init__(self, directory, scale = (16, 16)):
        self.directory = directory
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        self.tiles = {}
        for name in files:
            if name.split('.')[-1] == 'json':
                #image = pygame.image.load(os.path.join(directory, name)[0:-5] + '.png').convert_alpha()
                #self.image= image # tests
                self.tiles[name[0:-5]] = os.path.join(self.directory, name[0:-5]) + '.png', os.path.join(self.directory, name)
    def GetTile(self, name, parent, id):
        return Tile(parent, id, self.tiles[name][0], self.tiles[name][1], self, name)

        

class Layer(wx.Panel):
    def __init__(self, parent, id, metaset, grid):
        super().__init__(parent, id)
        self.metaset = metaset
        self.grid = grid
        sizer = wx.GridSizer(len(grid), len(grid[0]), 0, 0)
        self.SetSizer(sizer)
        for y in range(len(grid[0])):
            for x in range(len(grid)):
                name = metaset[grid[x][y]]
                tile = name[0].GetTile(name[1], self, -1)
                sizer.Add(tile, flag=wx.EXPAND)
    def Json(self):
        return {'metaset': self.metaset, 'grid': self.grid}
    def ReplaceTile(self, x, y, tileset, name):
        try:
            index = self.metaset.index((tileset, name))
        except ValueError:
            index = len(tileset)
            self.metaset.append((tileset, name))
        self.grid[x][y] = index
        self.sizer.Replace(self.sizer.GetItem(x + y * len(self.grid[0])), tileset.GetTile(name, self, -1))
    def GetTile(self, x, y):
        return self.sizer.GetItem(x + y * len(self.grid[0]))

class Tile(wxobjects.Physics):
    def __init__(self, parent, id, png, properties, tileset, name):
        super().__init__(parent, id)
        self.image = wx.Bitmap(png, wx.BITMAP_TYPE_ANY)
        sized = Tile.scale(self.image, self.GetSize().width, self.GetSize().height)
        self.static = wx.StaticBitmap(self, -1, sized)
        self.static.Show()
        self.tileset = tileset
        self.name = name
        self.Bind(wx.EVT_SIZE, self.onSize)

        f = open(properties, 'r')
        self.properties = json.load(f)
        f.close()

    def onSize(self, event):
        self.Resize()
        event.Skip()
        print(self.GetPosition(), self.GetSize())

    def Resize(self):
        self.static.Hide()
        sized = Tile.scale(self.image, self.GetSize().width, self.GetSize().height)
        self.static = wx.StaticBitmap(self, -1, sized)
        self.static.Show()

    def scale(bitmap, width, height):
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_NEAREST)
        result = image.ConvertToBitmap()
        return result
    def Collide(self, other):
        if Tile in other.collides:
            if (other.velocity[0]) > 0 and self.properties['solidity'] & 4:
                other.velocity[0] = self.velocity[0]
            elif (other.velocity[0]) < 0 and self.properties['solidity'] & 1:
                other.velocity[0] = self.velocity[0]
            if (other.velocity[1]) > 0 and self.properties['solidity'] & 2:
                other.velocity[1] = self.velocity[1]
                other.floor = True
            elif (other.velocity[1]) < 0 and self.properties['solidity'] & 8:
                other.velocity[1] = self.velocity[1]
                

