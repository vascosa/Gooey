import sys
from itertools import chain

import wx

from gooey.gui import events
from gooey.gui.components.header import FrameHeader
from gooey.gui.components.footer import Footer
from gooey.gui.util import wx_util
from gooey.gui.components.config import ConfigPage, TabbedConfigPage
from gooey.gui.components.sidebar import Sidebar
from gooey.gui.components.tabbar import Tabbar
from gooey.util.functional import getin, assoc, flatmap, compact
from gooey.python_bindings import constants
from gooey.gui.pubsub import pub
from gooey.gui import cli
from gooey.gui.components.console import Console
from gooey.gui.lang.i18n import _
from gooey.gui.processor import ProcessController
from gooey.gui.util.wx_util import transactUI


class GooeyApplication(wx.Frame):

    def __init__(self, buildSpec, *args, **kwargs):
        super(GooeyApplication, self).__init__(None, *args, **kwargs)
        self._state = {}
        self.buildSpec = buildSpec

        self.header = FrameHeader(self, buildSpec)
        self.configs = self.buildConfigPanels(self)
        self.navbar = self.buildNavigation()
        self.footer = Footer(self, buildSpec)
        self.console = Console(self)
        self.layoutComponent()

        self.clientRunner = ProcessController(
            self.buildSpec.get('progress_regex'),
            self.buildSpec.get('progress_expr')
        )

        pub.subscribe(events.WINDOW_STOP, self.onStop)
        pub.subscribe(events.WINDOW_CLOSE, self.onClose)
        pub.subscribe(events.WINDOW_START, self.onStart)
        pub.subscribe(events.WINDOW_EDIT, self.onEdit)
        pub.subscribe(events.CONSOLE_UPDATE, self.console.logOutput)
        pub.subscribe(events.EXECUTION_COMPLETE, self.onComplete)

    # def confirmStop(self):
    #     if self.view.confirm_stop_dialog():
    #         self.stop()
    #         return True
    #     return False

    def onStart(self, *args, **kwarg):
        """
        Verify user input and kick off the client's program if valid
        """
        with transactUI(self):
            config = self.navbar.getActiveConfig()
            config.resetErrors()
            if config.isValid():
                self.clientRunner.run(self.buildCliString())
                self.showConsole()
            else:
                config.displayErrors()
                self.Layout()

    def onEdit(self):
        """Return the user to the settings screen for futher editing"""
        with transactUI(self):
            self.showSettings()


    def buildCliString(self):
        """
        Collect all of the required information from the config screen and
        build a CLI string which can be used to invoke the client program
        """
        config = self.navbar.getActiveConfig()
        group = self.buildSpec['widgets'][self.navbar.getSelectedGroup()]
        positional = config.getPositionalArgs()
        optional = config.getOptionalArgs()

        return cli.buildCliString(
            self.buildSpec['target'],
            group['command'],
            positional,
            optional
        )


    def onComplete(self, *args, **kwargs):
        """
        Display the appropriate screen based on the success/fail of the
        host program
        """
        with transactUI(self):
            if self.clientRunner.was_success():
                self.showSuccess()
            else:
                self.showError()


    def onStop(self):
        print("Gunna stop!!")
        self.clientRunner.stop()

        import sys
        # sys.exit(1)
        # if self.view.confirm_exit_dialog():
        #     self.view.Destroy()
        #     sys.exit()

    def onClose(self):
        self.Destroy()
        sys.exit()


    def layoutComponent(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.header, 0, wx.EXPAND)
        sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)

        sizer.Add(self.navbar, 1, wx.EXPAND)
        sizer.Add(self.console, 1, wx.EXPAND)
        sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)
        sizer.Add(self.footer, 0, wx.EXPAND)
        self.SetMinSize((400, 300))
        self.SetSize(self.buildSpec['default_size'])
        self.SetSizer(sizer)
        self.console.Hide()
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
        def foo2(group):
            if not group:
                return []
            return group['items'] + flatmap(foo2, group['groups'])

        return {
            cmdKey: flatmap(foo2, group['contents'])
            for cmdKey, group in buildSpec['widgets'].items()
        }


    def showSettings(self):
        self.navbar.Show(True)
        self.console.Show(False)
        self.header.setImage('settings_img')
        self.header.setTitle(_("settings_title"))
        self.header.setSubtitle(self.buildSpec['program_description'])
        self.footer.showButtons('cancel_button', 'start_button')


    def showConsole(self):
        self.navbar.Show(False)
        self.console.Show(True)
        self.header.setImage('running_img')
        self.header.setTitle(_("running_title"))
        self.header.setSubtitle(_('running_msg'))
        self.footer.showButtons('stop_button')
        self.footer.progress_bar.Show(True)


    def showComplete(self):
        self.navbar.Show(False)
        self.console.Show(True)
        self.footer.showButtons('edit_button', 'restart_button', 'close_button')
        self.footer.progress_bar.Show(False)


    def showSuccess(self):
        self.showComplete()
        self.header.setImage('check_mark')
        self.header.setTitle(_('finished_title'))
        self.header.setSubtitle(_('finished_msg'))
        self.Layout()


    def showError(self):
        self.showComplete()
        self.header.setImage('error_symbol')
        self.header.setTitle(_('finished_title'))
        self.header.setSubtitle(_('finished_error'))



