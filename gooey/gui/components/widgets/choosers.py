from gooey.gui.components.widgets import core
from gooey.gui.components.widgets.bases import TextContainer, BaseChooser


class FileChooser(BaseChooser):
    # todo: allow wildcard from argparse
    widget_class = core.FileChooser


class FileSaver(BaseChooser):
    # todo: allow wildcard
    widget_class = core.FileSaver


class DirChooser(BaseChooser):
    # todo: allow wildcard
    widget_class = core.DirChooser


class DateChooser(BaseChooser):
    # todo: allow wildcard
    widget_class = core.DateChooser

