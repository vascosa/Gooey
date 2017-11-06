from gooey.gui.components.widgets.core.text_input import PasswordInput
from gooey.gui.components.widgets.textfield import TextField


__ALL__ = ('PasswordField',)

class PasswordField(TextField):
    widget_class = PasswordInput

