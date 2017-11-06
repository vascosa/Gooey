import wx

from gooey.gui.components.header import FrameHeader
from gooey.gui.components.footer import Footer
from gooey.gui.util import wx_util
from gui.components.config import ConfigPage
from util.functional import getin


class GooeyApplication(wx.Frame):

    def __init__(self, build_spec, *args, **kwargs):
        super(GooeyApplication, self).__init__(None, *args, **kwargs)
        self.build_spec = build_spec

        self.header = FrameHeader(self, build_spec)
        self.body = ConfigPage(self, build_spec)
        self.footer = Footer(self, build_spec)
        self.layoutComponent()

    def layoutComponent(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.header, 0, wx.EXPAND)
        sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)
        sizer.Add(self.body, 1, wx.EXPAND)
        sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)
        sizer.Add(self.footer, 0, wx.EXPAND)
        self.SetMinSize((400, 300))
        self.SetSize(self.build_spec['default_size'])


        # if self.layout_type == layouts.COLUMN:
        #     self.config_panel = layouts.ColumnLayout(self)
        # else:
        #     self.config_panel = layouts.FlatLayout(self)
        #
        # sizer.Add(self.config_panel, 1, wx.EXPAND)
        #
        # sizer.Add(self.runtime_display, 1, wx.EXPAND)
        #
        # self.runtime_display.Hide()
        # sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)
        # sizer.Add(self.foot_panel, 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

        # self.sizer = sizer




