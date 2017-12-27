import sys
import wx

from gooey.gui import events
from gooey.gui.components.header import FrameHeader
from gooey.gui.components.footer import Footer
from gooey.gui.util import wx_util
from gooey.gui.components.config import ConfigPage, TabbedConfigPage
from gooey.gui.components.sidebar import Sidebar
from gooey.gui.components.tabbar import Tabbar
from gooey.util.functional import getin, assoc
from gooey.python_bindings import constants
from gooey.gui.pubsub import pub



class GooeyApplication(wx.Frame):

    def __init__(self, buildSpec, *args, **kwargs):
        super(GooeyApplication, self).__init__(None, *args, **kwargs)
        self._state = {}
        self.buildSpec = buildSpec

        self.header = FrameHeader(self, buildSpec)
        self.configs = self.buildConfigPanels(self)
        self.navbar = self.buildNavigation()
        self.footer = Footer(self, buildSpec)
        self.layoutComponent()

        # eee = events

        pub.subscribe(events.WINDOW_CANCEL, self.onStop)
        pub.subscribe(events.WINDOW_CLOSE, self.onClose)
        pub.subscribe(events.WINDOW_START, self.onStart)
        pub.subscribe(events.USER_INPUT, self.updateState)


    def updateState(self, *args, **kwargs):
        self._state = assoc(self._state, kwargs.get('id'), kwargs)
        import pprint
        pprint.pprint(self._state)
        print('\n======\n')


    def onStart(self, *args, **kwarg):
        self._state.values()


    def onStop(self):
        print("Gunna stop!!")
        # if self.view.confirm_exit_dialog():
        #     self.view.Destroy()
        #     sys.exit()

    def onClose(self):
        self.Destroy()
        sys.exit()


    def handleButtonNavigation(self, *args, **kwargs):
        print('Howdy!:', args, kwargs)


    def layoutComponent(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.header, 0, wx.EXPAND)
        sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)

        sizer.Add(self.navbar, 1, wx.EXPAND)
        sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)
        sizer.Add(self.footer, 0, wx.EXPAND)
        self.SetMinSize((400, 300))
        self.SetSize(self.buildSpec['default_size'])
        self.SetSizer(sizer)
        self.Layout()


    def buildNavigation(self):
        if self.buildSpec['navigation'] == constants.TABBED:
            navigation = Tabbar(self, self.buildSpec, self.configs)
        else:
            navigation = Sidebar(self, self.buildSpec, self.configs)
            if self.buildSpec['navigation'] == constants.HIDDEN:
                navigation.Hide()
        return navigation


    def buildConfigPanels(self, parent):
        page_class = TabbedConfigPage if self.buildSpec['tabbed_groups'] else ConfigPage

        return [page_class(parent, widgets)
                for widgets in self.buildSpec['widgets'].values()]


    def flattenWidgets(self, buildSpec):

        def extractWidgets(group):
            if not group.get('groups'):
                return []
            else:
                return [item for item in group['items']] + \
                       extractWidgets(group.get('groups'))
        return {
            cmdKey: extractWidgets(group)
            for cmdKey, cmdGroup in buildSpec['widgets'].items()
            for group in cmdGroup['contents']
        }


