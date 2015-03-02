#! python


__version__     = '0.1'
__author__      = ('linkedin.com/in/danielforgacs; '
                    'github.com/danielforgacs; '
                    'bitbucket.org/fordan')


__doc__         = """/
Houdini scene setup for pipeline integration

Houdini version: 14.0
Python version: H14.0 default
"""

# Notes:

# hou.appendSessionModuleSource, hou.hipFile
# hou.isUIAvailable, hou.lvar


import os
import sys
import hou


_DEBBUG = True


def _message(text, value = '', debug = True):
    """printing unified info & debug messages"""

    # print ('--> {}: {}'.format(text, value))
    if debug:
        print '--> %s: %s' % (text, value)


class SysEnv(object):
    """system base class
    to get user name and other env vars"""

    def __init__(self):
        pass

    def get_os(self):
        return sys.platform

    def get_user(self):
        return os.getlogin()


class Shot(SysEnv):
    """shot base class
    general project & shot methods
    like framerange, folders, naming"""

    def __init__(self):
        pass

    def get_project(self):
        pass

    def get_shot(self):
        pass


class HouWorkEnv(Shot):
    """Base Houdini Scene Class
    for Houdini scene methods"""

    def __init__(self, startframe = 1, endframe = 48):
        self.set_frame_range(startframe, endframe)

        if int(hou.fps()) != 24:
            text = 'frame rate is not 24 fps\nfps = %s' % hou.fps()
            hou.ui.displayMessage(text)

    def set_frame_range(self, startframe, endframe):
        begin       = (startframe - 1) / hou.fps()
        end         = endframe / hou.fps()

        hou.hscript('tset %s %s' % (begin, end))

        self.set_play_range(startframe, endframe)

    def set_play_range(self, rfstart, rfend):
        hou.playbar.setPlaybackRange(rfstart, rfend)
        hou.playbar.setRealTime(True)

    def set_preroll(self, frames):
        pass


if __name__ == '__main__':
    pass


# TEST PART
_message('debug mode', debug = _DEBBUG)
_message('==> HouWorkEnv module test', debug = _DEBBUG)

h = HouWorkEnv()
exs = hou.expandString
_message('frame range: %s - %s' % (exs('$FSTART'), exs('$FEND')))
_message('play range: %s - %s' % (exs('$RFSTART'), exs('$RFEND')))