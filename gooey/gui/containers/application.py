import wx

from gooey.gui.components.header import FrameHeader
from gooey.gui.components.footer import Footer
from gooey.gui.util import wx_util
from gui.components.config import ConfigPage
from gui.components.sidebar import Sidebar
from util.functional import getin


class GooeyApplication(wx.Frame):

    def __init__(self, build_spec, *args, **kwargs):
        super(GooeyApplication, self).__init__(None, *args, **kwargs)
        self.build_spec = build_spec

        self.header = FrameHeader(self, build_spec)
        self.sidebar = Sidebar(self, build_spec)
        self.configs = self.buildConfigPanels()
        self.footer = Footer(self, build_spec)
        self.layoutComponent()

    def layoutComponent(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.header, 0, wx.EXPAND)
        sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)

        sizer.Add(self.layoutBody(), 1, wx.EXPAND)
        sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)
        sizer.Add(self.footer, 0, wx.EXPAND)
        self.SetMinSize((400, 300))
        self.SetSize(self.build_spec['default_size'])
        self.SetSizer(sizer)
        self.Layout()


    def layoutBody(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.sidebar, 0, wx.EXPAND)
        for body in self.configs:
            hsizer.Add(body, 1, wx.EXPAND)
            body.Hide()
        self.configs[1].Show()
        return hsizer


    def buildConfigPanels(self):
        return [ConfigPage(self, widgets)
                for widgets in self.build_spec['widgets'].values()]




