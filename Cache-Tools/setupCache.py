#! python

__version__     = '0.2'
__author__      = 'forgacs.daniel@gmail.com'

"""
tested:     Houdini version 14.0
python:     H14 default
"""

import hou


def setup_cache():
    nodes           = { 'geo'   : hou.selectedNodes()[0],
                        'root'  : hou.node('/obj')}
    
    nodes['null']   = nodes['geo'].createOutputNode('null', 'TO_CACHE_')
    nodes['read']   = nodes['null'].createOutputNode('file')

    for code in ('setDisplayFlag', 'setRenderFlag'):
        eval('nodes["read"].%s(True)' % (code))
    
    parmtemplate    = hou.StringParmTemplate("rop", "rop", 1,
                            string_type = hou.stringParmType.NodeReference)

    nodes['read'].addSpareParmTuple(parmtemplate)
    nodes['read'].parm("filemode").lock(True)
    nodes['read'].parm('file').set('`chs(chs("rop") + "/sopoutput")`')
    nodes['read'].setCurrent(True, clear_all_selected = True)

    if nodes['root'].node('cache'):
        nodes['ropnet']  = nodes['root'].node('cache')
    else:
        nodes['ropnet']  = nodes['root'].createNode('ropnet', 'cache')

    nodes['rop'] = nodes['ropnet'].createNode('geometry', nodes['geo'].name())
    nodes['read'].parm('rop').set(nodes['rop'].path())

    rop_parms   = {'soppath'    : nodes['null'].path(),
                    'sopoutput' : '{0}/$OS/$OS.$F4.bgeo.sc'.format('$CACHE'),
                    'trange'    : 2,
                    'mkpath'    : True,
                    'saveretry' : 2,
                    '@f1'       : '$FSTART',
                    '@f2'       : '$FEND + 1'
                    }

    for key in rop_parms:
        if '@' not in key:
            nodes['rop'].parm(key).set(rop_parms[key])

        else:
            nodes['rop'].parm(key[1:]).setExpression(rop_parms[key])