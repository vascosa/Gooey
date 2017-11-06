import wx
from wx.lib.scrolledpanel import ScrolledPanel
from util.functional import getin


class ConfigPage(ScrolledPanel):
    def __init__(self, parent, buildSpec, *args, **kwargs):
        super(ConfigPage, self).__init__(parent, *args, **kwargs)
        self.SetupScrolling(scroll_x=False, scrollToTop=False)
        self.buildSpec = buildSpec
        self.layoutComponent()


    def layoutComponent(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        for key, group in self.buildSpec['widgets'].items():
            [self.makeGroup(sizer, item, 0, wx.EXPAND) for item in group['contents']]

        self.SetSizer(sizer)

    def makeGroup(self, thissizer, group, *args):
        if getin(group, ['options', 'show_border'], True):
            boxDetails = wx.StaticBox(self, -1, group['name'])
            boxSizer = wx.StaticBoxSizer(boxDetails, wx.VERTICAL)
        else:
            boxSizer = wx.BoxSizer(wx.VERTICAL)

        ui_groups = []
        subgroup = []
        for index, item in enumerate(group['items']):
            if getin(item, ['options', 'full_width'], False):
                ui_groups.append(subgroup)
                ui_groups.append([item])
                subgroup = []
            else:
                subgroup.append(item)
            if len(subgroup) == getin(group, ['options', 'columns'], 2) \
                or item == group['items'][-1]:
                ui_groups.append(subgroup)
                subgroup = []

        from gooey.gui.components import widgets
        for uigroup in ui_groups:
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            for item in uigroup:
                # instantiate the widget type
                widgetClass = getattr(widgets, item['type'])
                widget = widgetClass(self, item)
                # tc = wx.TextCtrl(self)
                sizer.Add(widget, 1, wx.ALL | wx.EXPAND, 5)
            boxSizer.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)

        hs = wx.BoxSizer(wx.HORIZONTAL)
        for e, subgroup in enumerate(group['groups']):
            self.makeGroup(hs, subgroup, 1, wx.ALL | wx.EXPAND, 5)
            if e % getin(group, ['options', 'columns'], 2) \
                or e == len(group['groups']):
                boxSizer.Add(hs, *args)
                hs = wx.BoxSizer(wx.HORIZONTAL)

        thissizer.Add(boxSizer, *args)

        return boxSizer
