import wx
from gooey.gui.components.widgets.bases import TextContainer
from gui.util import wx_util


class CheckBox(TextContainer):

    widget_class = wx.CheckBox

    def arrange(self, *args, **kwargs):
        wx_util.make_bold(self.label)
        wx_util.dark_grey(self.help_text)
        self.help_text.SetMinSize((0,-1))

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.label)
        layout.AddSpacer(2)
        if self.help_text:
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            hsizer.Add(self.widget, 0)
            hsizer.Add(self.help_text, 1)
            layout.Add(hsizer, 1, wx.EXPAND)
            layout.AddSpacer(2)
        else:
            layout.Add(self.widget, 0, wx.EXPAND)
            layout.AddStretchSpacer(1)
        # layout.Add(self.getSublayout(), 0, wx.EXPAND)
        return layout

    def hideInput(self):
        self.widget.Hide()
