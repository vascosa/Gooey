'''
Created on Dec 23, 2013

@author: Chris
'''

import wx

from gooey.gui import imageutil, image_repository
from gooey.gui.util import wx_util
from gui.three_to_four import bitmapFromImage
from util.functional import getin

PAD_SIZE = 10


class FrameHeader(wx.Panel):
    def __init__(self, parent, build_spec, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)
        self.SetDoubleBuffered(True)

        self.build_spec = build_spec

        self._header = None
        self._subheader = None
        self.settings_img = None
        self.running_img = None
        self.check_mark = None
        self.error_symbol = None

        self.layoutComponent()


    def setTitle(self, title):
        pass

    def setSubtitle(self, subtitle):
        pass

    def setImage(self, image):
        pass


    def layoutComponent(self):

        self.SetBackgroundColour(self.build_spec['header_bg_color'])
        self.SetSize((30, self.build_spec['header_height']))
        self.SetMinSize((120, self.build_spec['header_height']))

        self._header = wx_util.h1(self, '')
        self._subheader = wx.StaticText(self, label='')

        images = self.build_spec['images']
        targetHeight = self.build_spec['header_height'] - 10
        self.settings_img = self._load_image(images['configIcon'], targetHeight)
        self.running_img = self._load_image(images['runningIcon'], targetHeight)
        self.check_mark = self._load_image(images['successIcon'], targetHeight)
        self.error_symbol = self._load_image(images['errorIcon'], targetHeight)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        headings_sizer = self.build_heading_sizer()
        sizer.Add(headings_sizer, 1,
                  wx.ALIGN_LEFT | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.LEFT,
                  PAD_SIZE)
        sizer.Add(self.settings_img, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT, PAD_SIZE)
        sizer.Add(self.running_img, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT, PAD_SIZE)
        sizer.Add(self.check_mark, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT, PAD_SIZE)
        sizer.Add(self.error_symbol, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT, PAD_SIZE)
        self.running_img.Hide()
        self.check_mark.Hide()
        self.error_symbol.Hide()
        vsizer.Add(sizer, 1, wx.EXPAND)
        self.SetSizer(vsizer)


    def _load_image(self, imgPath, targetHeight):
        rawImage = imageutil.loadImage(imgPath)
        sizedImage = imageutil.resizeImage(rawImage, targetHeight)
        return imageutil.wrapBitmap(sizedImage, self)


    def build_heading_sizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer(1)
        sizer.Add(self._header, 0)
        sizer.Add(self._subheader, 0)
        sizer.AddStretchSpacer(1)
        return sizer
