import wx
from gooey.gui.components.widgets.bases import BaseWidget
from gooey.gui.util import wx_util
from gooey.gui.components.widgets import CheckBox
from gooey.util.functional import getin, findfirst


class RadioGroup(BaseWidget):

    def __init__(self, parent, widgetInfo, *args, **kwargs):
        super(RadioGroup, self).__init__(parent, *args, **kwargs)
        self._parent = parent
        self.info = widgetInfo
        self._id = widgetInfo['id']
        self.widgetInfo = widgetInfo
        self.error = wx.StaticText(self, label='')
        self.radioButtons = self.createRadioButtons()
        self.selected = None
        self.widgets = self.createWidgets()
        self.arrange()
        self.applyStyleRules()

        for button in self.radioButtons:
            button.Bind(wx.EVT_LEFT_DOWN, self.handleButtonClick)


    def getValue(self):
        for button, widget in zip(self.radioButtons, self.widgets):
            if button.GetValue():  # is Checked
                print('Button was checked!')
                return widget.getValue()
        else:
            # just return the first widget's value even though it's
            # not active so that the expected interface is satisfied
            return self.widgets[0].getValue()

    def setErrorString(self, message):
        self.error.SetLabel(message)
        self.error.Wrap(self.Size.width)

    def showErrorString(self, b):
        self.error.Wrap(self.Size.width)
        self.error.Show(b)


    def arrange(self, *args, **kwargs):
        title = getin(self.widgetInfo, ['options', 'title'], 'Choose One')
        if getin(self.widgetInfo, ['options', 'show_border'], False):
            boxDetails = wx.StaticBox(self, -1, title)
            boxSizer = wx.StaticBoxSizer(boxDetails, wx.VERTICAL)
        else:
            boxSizer = wx.BoxSizer(wx.VERTICAL)
            boxSizer.AddSpacer(10)
            boxSizer.Add(wx_util.h1(self, title), 0)

        for btn, widget in zip(self.radioButtons, self.widgets):
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(btn,0, wx.RIGHT, 4)
            sizer.Add(widget, 1, wx.EXPAND)
            boxSizer.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(boxSizer)


    def handleButtonClick(self, event):
        if event.EventObject.Id == getattr(self.selected, 'Id', None):
            event.EventObject.SetValue(False)
        else:
            self.selected = event.EventObject
            self.selected.SetValue(True)
        self.applyStyleRules()

    def applyStyleRules(self):
        """
        Conditionally disabled/enables form fields based on the current
        section in the radio group
        """
        for button, widget in zip(self.radioButtons, self.widgets):
            if isinstance(widget, CheckBox):
                widget.hideInput()
            if not button.GetValue(): # checked
                widget.widget.Disable()
            else:
                widget.widget.Enable()

    def createRadioButtons(self):
        # button groups in wx are statefully determined via a style flag
        # on the first button (what???). All button instances are part of the
        # same group until a new button is created with the style flag RG_GROUP
        # https://wxpython.org/Phoenix/docs/html/wx.RadioButton.html
        # (What???)
        firstButton = wx.RadioButton(self, style=wx.RB_GROUP)
        firstButton.SetValue(False)
        buttons = [firstButton]

        for _ in getin(self.widgetInfo, ['data','widgets'], [])[1:]:
            buttons.append(wx.RadioButton(self))
        return buttons

    def createWidgets(self):
        """
        Instantiate the Gooey Widgets that are used within the RadioGroup
        """
        from gooey.gui.components import widgets
        return [getattr(widgets, item['type'])(self, item)
                for item in getin(self.widgetInfo, ['data', 'widgets'], [])]
