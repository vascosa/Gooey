import wx
# from rx.subjects import Subject

from gooey.gui import formatters, events
from gooey.gui.pubsub import pub
from gooey.gui.util import wx_util
from gooey.util.functional import getin


class BaseWidget(wx.Panel):
    widget_class = None

    def arrange(self, label, text):
        raise NotImplementedError

    def getWidget(self, parent, **options):
        return self.widget_class(parent, **options)

    def connectSignal(self):
        raise NotImplementedError

    def getSublayout(self, *args, **kwargs):
        raise NotImplementedError

    def setValue(self, value):
        raise NotImplementedError

    def receiveChange(self, *args, **kwargs):
        raise NotImplementedError

    def dispatchChange(self, value, **kwargs):
        raise NotImplementedError

    def formatOutput(self, metatdata, value):
        raise NotImplementedError


class TextContainer(BaseWidget):
    widget_class = None

    def __init__(self, parent, widgetInfo, *args, **kwargs):
        super(TextContainer, self).__init__(parent, *args, **kwargs)

        self._id = widgetInfo['id']
        self._meta = widgetInfo['data']
        self._options = widgetInfo['options']
        self.label = wx.StaticText(self, label=widgetInfo['data']['display_name'])
        self.help_text = wx.StaticText(self, label=widgetInfo['data']['help'] or '')
        self.error = wx.StaticText(self, label='asdf adsf asdf adsf asdf asdf ')
        self.widget = self.getWidget(self)
        self.layout = self.arrange(*args, **kwargs)
        self.SetSizer(self.layout)
        # self.error.Hide()
        # self.value = Subject()
        self.connectSignal()

    def arrange(self, *args, **kwargs):
        wx_util.make_bold(self.label)
        wx_util.dark_grey(self.help_text)
        wx_util.withColor(self.error, self._options['error_color'])

        self.help_text.SetMinSize((0,-1))

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.label)
        layout.AddSpacer(2)
        if self.help_text:
            layout.Add(self.help_text, 1, wx.EXPAND)
            layout.AddSpacer(2)
        else:
            layout.AddStretchSpacer(1)
        layout.Add(self.getSublayout(), 0, wx.EXPAND)
        layout.Add(self.error, 1, wx.EXPAND)
        return layout

    def getWidget(self, *args, **options):
        return self.widget_class(*args, **options)

    def connectSignal(self):
        self.widget.Bind(wx.EVT_TEXT, self.dispatchChange)

    def getSublayout(self, *args, **kwargs):
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.widget, 1, wx.EXPAND)
        return layout

    def getValue(self):
        raise NotImplementedError

    def setValue(self, value):
        raise NotImplementedError

    def receiveChange(self, metatdata, value):
        raise NotImplementedError

    def dispatchChange(self, value, **kwargs):
        raise NotImplementedError

    def formatOutput(self, metadata, value):
        raise NotImplementedError


class BaseChooser(TextContainer):
    """ Base Class for the Chooser widget types """

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
