'''/
bakes houdini chanel expression into
keys onn each frame in the timeline

todo:

- chanels as arguments
- check and get leyframes'''


__version__     = 'v0.1'
__author__      = 'github/danielforgacs'


import hou


def bakeParm():
    node        = hou.node('/obj/sphere')
    parm        = node.parm('rx')
    values      = []
    start, end  = get_frame_range()
    
    for k in range(2):
        for frame in range( start, end + 1):
#            print frame

            if k == 0:
                values.append( parm.evalAtFrame(frame))

            else:
                if frame == start:
                    parm.deleteAllKeyframes()
                value       = hou.Keyframe()
                
                value.setFrame(frame)
                value.setValue(values[frame - 1])
                print value.value
                parm.setKeyframe(value)


def get_frame_range():
    return (1, 50)


bakeParm()