from gooey.gui.components.widgets.bases import TextContainer
import wx

from gooey.gui import formatters


class Dropdown(TextContainer):

    def getWidget(self, parent, *args, **options):
        default = 'Select Option'
        return wx.ComboBox(
            parent=parent,
            id=-1,
            value=default,
            choices=[default] + self._meta['choices'],
            style=wx.CB_DROPDOWN)

    def getWidgetValue(self):
        return self.widget.GetValue()


    def formatOutput(self, metadata, value):
        return formatters.dropdown(metadata, value)
