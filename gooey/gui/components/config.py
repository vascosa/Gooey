import wx
from wx.lib.scrolledpanel import ScrolledPanel

from gooey.gui.util import wx_util
from gooey.util.functional import getin


class ConfigPage(ScrolledPanel):
    def __init__(self, parent, rawWidgets, *args, **kwargs):
        super(ConfigPage, self).__init__(parent, *args, **kwargs)
        self.SetupScrolling(scroll_x=False, scrollToTop=False)
        self.rawWidgets = rawWidgets
        self.layoutComponent()


    def layoutComponent(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        for item in self.rawWidgets['contents']:
            self.makeGroup(self, sizer, item, 0, wx.EXPAND)
        self.SetSizer(sizer)


    def makeGroup(self, parent, thissizer, group, *args):
        if getin(group, ['options', 'show_border'], False):
            boxDetails = wx.StaticBox(parent, -1, group['name'])
            boxSizer = wx.StaticBoxSizer(boxDetails, wx.VERTICAL)
        else:
            boxSizer = wx.BoxSizer(wx.VERTICAL)
            boxSizer.AddSpacer(10)
            boxSizer.Add(wx_util.h1(parent, group['name']), 0, wx.TOP | wx.BOTTOM | wx.LEFT, 8)

        group_description = getin(group, ['description'])
        if group_description:
            description = wx.StaticText(parent, label=group_description)
            boxSizer.Add(description, 0,  wx.EXPAND | wx.LEFT, 10)

        # apply an underline when a grouping border is not specified
        if not getin(group, ['options', 'show_border'], False):
            boxSizer.Add(wx_util.horizontal_rule(parent), 0, wx.EXPAND | wx.LEFT, 10)

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
                widget = widgetClass(parent, item)
                sizer.Add(widget, 1, wx.ALL | wx.EXPAND, 5)
            boxSizer.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)

        hs = wx.BoxSizer(wx.HORIZONTAL)
        for e, subgroup in enumerate(group['groups']):
            self.makeGroup(parent, hs, subgroup, 1, wx.ALL | wx.EXPAND, 5)
            if e % getin(group, ['options', 'columns'], 2) \
                or e == len(group['groups']):
                boxSizer.Add(hs, *args)
                hs = wx.BoxSizer(wx.HORIZONTAL)

        thissizer.Add(boxSizer, *args)

        return boxSizer



class TabbedConfigPage(ConfigPage):
    """
    Splits top-level groups across tabs
    """
    def __init__(self, parent, rawWidgets, *args, **kwargs):
        super(ConfigPage, self).__init__(parent, *args, **kwargs)
        self.SetupScrolling(scroll_x=False, scrollToTop=False)
        self.rawWidgets = rawWidgets
        self.layoutComponent()


    def layoutComponent(self):
        # self.rawWidgets['contents'] = self.rawWidgets['contents'][1:2]
        self.notebook = wx.Notebook(self, style=wx.BK_DEFAULT)

        panels = [wx.Panel(self.notebook) for _ in self.rawWidgets['contents']]
        sizers = [wx.BoxSizer(wx.VERTICAL) for _ in panels]

        for group, panel, sizer in zip(self.rawWidgets['contents'], panels, sizers):
            self.makeGroup(panel, sizer, group, 0, wx.EXPAND)
            panel.SetSizer(sizer)
            panel.Layout()
            self.notebook.AddPage(panel, group['name'])
            self.notebook.Layout()


        _sizer = wx.BoxSizer(wx.VERTICAL)
        _sizer.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(_sizer)
        self.Layout()




