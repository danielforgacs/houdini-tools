"""
bakes houdini chanel expression into
keys on each frame in the timeline

Houdini 15.0

todo:
    - automatical parm selection
"""


__version__     = 'v0.3'
__author__      = 'github/danielforgacs'


import hou


def bake_parm(parm):
    values          = []
    start, end      = get_frame_range()
    end             += 1

    values          = get_values(start, end, parm)
    parm.deleteAllKeyframes()
    bake_values(start, end, parm, values)


def get_values(start, end, parm):
    vals    = []

    for frame in range( start, end):
        vals.append(parm.evalAtFrame(frame))

    return vals


def bake_values(start, end, parm, values):
    for frame in range( start, end):
        keyframe       = hou.Keyframe()
        keyframe.setValue(values[frame - start])
        keyframe.setFrame(frame)
        keyframe.setExpression('spline()')

        parm.setKeyframe(keyframe)


def get_frame_range():
    get                 = hou.expandString
    start, end          = (int(get('$FSTART')), int(get('$FEND')))

    return (start, end)


def main():
    parm = hou.parm('/obj/geo1/rx')
    bake_parm(parm)
