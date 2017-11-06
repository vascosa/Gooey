'''
Collection of the image paths.

The module is meant to act as a singleton, hence the globals() abuse.

Image credit: kidcomic.net
'''
import os
from functools import partial

from gooey.gui.util.freeze import getResourcePath



filenames = {
    'programIcon': 'program_icon.ico',
    'successIcon': 'success_icon.png',
    'runningIcon': 'running_icon.png',
    'loadingIcon': 'loading_icon.gif',
    'configIcon': 'config_icon.png',
    'errorIcon': 'error_icon.png'
}


def loadImages(targetDir):
    defaultImages = resolvePaths(getResourcePath('images'), filenames)
    return {'images': maybePatchImagePaths(targetDir, defaultImages)}


def getImageDirectory(targetDir):
    return getResourcePath('images') \
           if targetDir == 'default' \
           else targetDir


def maybePatchImagePaths(targetDir, imagemap):
    '''
    Overrides the stock images with any custom images
    found in the user supplied directory
    '''
    if targetDir == 'default':
        return imagemap

    pathto = partial(os.path.join, targetDir)
    if not os.path.isdir(targetDir):
        raise IOError('Unable to find the user supplied directory {}'.format(
            targetDir))

    return {varname: pathto(filename)
            for varname, filename in imagemap.items()
            if os.path.exists(pathto(filename))}


def resolvePaths(dirname, filenames):
    return {key:  os.path.join(dirname, filename)
            for key, filename in filenames.items()}


