from gooey.gui.components.widgets.bases import TextContainer
import wx

class Dropdown(TextContainer):

    def getWidget(self, parent, *args, **options):
        default = 'Select Option'
        return wx.ComboBox(
            parent=parent,
            id=-1,
            value=default,
            choices=[default] + self._meta['choices'],
            style=wx.CB_DROPDOWN)
