from gooey.gui.components.widgets.bases import TextContainer
import wx

class Listbox(TextContainer):

    def getWidget(self, parent, *args, **options):
        default = 'Select Option'
        return wx.ListBox(
            parent=parent,
            choices=self._meta['choices'],
            size=(-1,60),
            style=wx.LB_MULTIPLE
        )


