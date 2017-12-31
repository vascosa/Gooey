from collections import namedtuple

import wx


DialogConstants = namedtuple('DialogConstants', 'YES NO', [5103, 5104])


def showDialog(title, content, style):
    dlg = wx.MessageDialog(None, content, title, style)
    result = dlg.ShowModal()
    dlg.Destroy()
    return result


def missingArgsDialog():
    showDialog(_('error_title'), _('error_required_fields'), wx.ICON_ERROR)


def validationFailure():
    showDialog(_('error_title'), _('validation_failed'), wx.ICON_WARNING)


def confirmExit():
    result = showDialog(_('sure_you_want_to_exit'), _('close_program'), wx.YES_NO)
    return result == DialogConstants.YES


def confirmForceStop():
    result = showDialog(_('sure_you_want_to_stop'), _('stop_task'), wx.YES_NO)
    return result == DialogConstants.YES
