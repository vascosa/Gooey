from gooey.gui.components.widgets.bases import TextContainer
import wx

from gui import formatters


class Listbox(TextContainer):

    def getWidget(self, parent, *args, **options):
        default = 'Select Option'
        return wx.ListBox(
            parent=parent,
            choices=self._meta['choices'],
            size=(-1,60),
            style=wx.LB_MULTIPLE
        )

    def setValue(self, values):
        for string in values:
            self.widget.SetStringSelection(string)

    def getWidgetValue(self):
        return [self.widget.GetString(index)
                for index in self.widget.GetSelections()]


    def formatOutput(self, metadata, value):
        return formatters.listbox(metadata, value)
