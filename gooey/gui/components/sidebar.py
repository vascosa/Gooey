import wx

from gooey.gui import events
from gooey.gui.pubsub import pub
from gooey.gui.util import wx_util


class Sidebar(wx.Panel):
    def __init__(self, parent, buildSpec, *args, **kwargs):
        super(Sidebar, self).__init__(parent, *args, **kwargs)
        self._parent = parent
        self.buildSpec = buildSpec
        self.options = list(self.buildSpec['widgets'].keys())
        self.label = wx_util.h1(self, self.buildSpec.get('subparser_title'))
        self.listbox = wx.ListBox(self, -1, choices = self.options)
        self.layoutComponent()

    def layoutComponent(self):
        self.SetBackgroundColour('#f2f2f2')
        self.SetSize((180, 0))
        self.SetMinSize((180, 0))

        container = wx.BoxSizer(wx.VERTICAL)
        container.AddSpacer(15)
        container.Add(self.label, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        container.AddSpacer(5)

        container.Add(self.listbox, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        container.AddSpacer(20)

        self.listbox.SetSelection(0)
        self.SetSizer(container)

        self.Bind(wx.EVT_LISTBOX, self.selectionChange, self.listbox)

    def selectionChange(self, evt):
        pub.send_message(
            events.LIST_BOX,
            selection=self.listbox.GetItems()[self.listbox.GetSelection()])
        evt.Skip()
