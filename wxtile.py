import wx
import json

class Tileset:
    def __init__(self, directory, scale = (16, 16)):
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        self.tiles = {}
        for name in files:
            print('file:', name) 
            if name.split('.')[-1] == 'json':
                print(name, 'is a json.')
                #image = pygame.image.load(os.path.join(directory, name)[0:-5] + '.png').convert_alpha()
                #self.image= image # tests
                self.tiles[name[0:-5]] = Tile(None, -1, os.path.join(directory, name)[0:-5] + '.png', os.path.join(directory, name))
                self.tiles[name[0:-5]].tileset = self

        

class Layer(wx.Panel):
    def __init__(self, parent, id, metaset, data):
        super().__init__(parent, id)
        self.sizer = wx.GridBagSizer
        for x in range(len(data)):
            for y in range(len(data[x])):
                self.sizer.Add(Tile(self, -1, 'graphics/SMW/grass/topleft.png', 'graphics/SMW/grass/topleft.json'), (x, y), flag=wx.EXPAND)

class Tile(wx.Panel):
    def __init__(self, parent, id, png, properties):
        super().__init__(parent, id)
        self.image = wx.Bitmap(png, wx.BITMAP_TYPE_ANY)
        sized = Tile.scale(self.image, self.GetSize().width, self.GetSize().height)
        self.static = wx.StaticBitmap(self, -1, sized)
        self.static.Show()
        self.tileset = None
        self.Bind(wx.EVT_SIZE, self.OnSize)

        f = open(properties, 'r')
        self.properties = json.load(f)
        f.close()

    def OnSize(self, event):
        self.static.Hide()
        sized = ScaledBitmap.scale(self.image, self.GetSize().width, self.GetSize().height)
        self.static = wx.StaticBitmap(self, -1, sized)
        self.static.Show()
        event.Skip()


    def scale(bitmap, width, height):
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_NEAREST)
        result = image.ConvertToBitmap()
        return result

