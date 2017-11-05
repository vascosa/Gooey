import wx
from gooey.gui.components.widgets.bases import TextContainer
from gooey.gui import formatters
from gooey.gui.components.widgets.core.text_input import TextInput


class TextField(TextContainer):
    widget_class = TextInput

    def setValue(self, value):
        self.widget.SetValue(value)

    def dispatchChange(self, value, **kwargs):
        self.value.on_next({
            'id': self._id,
            'cmd': self.formatOutput(self._meta, value),
            'rawValue': value
        })

    def formatOutput(self, metatdata, value):
        return formatters.general(metatdata, value)

