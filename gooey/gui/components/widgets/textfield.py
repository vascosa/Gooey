import wx
from gooey.gui.components.widgets.bases import TextContainer
from gooey.gui import formatters, events
from gooey.gui.components.widgets.core.text_input import TextInput
from gooey.gui.pubsub import pub


class TextField(TextContainer):
    widget_class = TextInput

    def setValue(self, value):
        self.widget.SetValue(value)

    def dispatchChange(self, event, **kwargs):
        value = event.EventObject.GetValue()
        pub.send_message(
            events.USER_INPUT,
            id=self._id,
            cmd=self.formatOutput(self._meta, value),
            rawValue=value
        )

    def formatOutput(self, metatdata, value):
        return formatters.general(metatdata, value)

