"""
=================================
set up caching for selected node.
=================================

tested:     Houdini version 15.0
python:     H15 default

ctrl click uses local cache.
ctrl alt click runs tests

shelf tool:
##########################################################
import sys

modulepath = '<MODULE PATH>'

if modulepath not in sys.path:
    sys.path.append(modulepath)


import setupcache
reload(setupcache)


if kwargs['altclick'] and kwargs['ctrlclick']:
    import uuid
    import setupcache_test
    reload(setupcache_test)
    print('\n\n--> running cache setup tests...')
    print('test id: ', uuid.uuid1())
    setupcache_test.main()
else:
    print('\n\n--> setting up cache...')
    setupcache.main(kwargs)
##########################################################
"""


__version__     = '0.5'
__author__      = 'forgacs.daniel@gmail.com'



try:
    import hou
except:
    pass


def setup_cache(localcache):
    nodes           = { 'geo'   : hou.selectedNodes()[0],
                        'root'  : hou.node('/obj')}

    if localcache:
        nodes['root']   = nodes['geo'].parent()

    nodes['null']   = nodes['geo'].createOutputNode('null', 'TO_CACHE_')
    nodes['read']   = nodes['null'].createOutputNode('file')

    nodes['read'].setDisplayFlag(True)
    nodes['read'].setRenderFlag(True)

    parmtemplate    = hou.StringParmTemplate('rop', 'rop', 1,
                            string_type = hou.stringParmType.NodeReference)

    nodes['read'].addSpareParmTuple(parmtemplate)
    nodes['read'].parm("filemode").lock(True)
    nodes['read'].parm('file').set('`chs(chs("rop") + "/sopoutput")`')
    nodes['read'].setCurrent(True, clear_all_selected = True)

    if nodes['root'].node('cache'):
        nodes['ropnet']  = nodes['root'].node('cache')
    else:
        nodes['ropnet']  = nodes['root'].createNode('ropnet', 'cache')

    nodes['ropnet'].moveToGoodPosition()

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

    if localcache:
        rop_parms['soppath'] = nodes['rop'].relativePathTo(nodes['null'])
        nodes['read'].parm('rop').set(nodes['read'].relativePathTo(nodes['rop']))
        # nodes['read'].parm('rop').set('111')

    for key in rop_parms:
        if '@' not in key:
            nodes['rop'].parm(key).set(rop_parms[key])

        else:
            nodes['rop'].parm(key[1:]).setExpression(rop_parms[key])



def get_sop_from_selection():
    sop = hou.selectedNodes()[0]

    return sop



def main(kwargs):
    localcache      = kwargs.get('ctrlclick', None)

    setup_cache(localcache)


def main2():
    sop = get_sop_from_selection()
    cacheout = sop.createOutputNode('output', 'TO_CACHE_' + sop.name())
    cachefile = cacheout.createOutputNode('file', 'CACHE_' + sop.name())

    cachefile.setSelected(True, clear_all_selected=True)
    cachefile.setCurrent(True, clear_all_selected=True)

    ropnet = sop.parent().createNode('ropnet', 'Cache_Ropnet')
    ropnet.createNode('geometry', sop.name())


if __name__ == '__main__':
    pass
