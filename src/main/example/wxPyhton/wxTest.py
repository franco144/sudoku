import wx

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        # wx.Frame.__init__(self, *args, **kw)
        self.panel = wx.Panel(self, wx.ID_ANY)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, title="wxPython Test")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()