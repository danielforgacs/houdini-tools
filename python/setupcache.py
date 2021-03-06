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

modulepath = 'c:\_store\dev\houdini-tools-env\houdini-tools\python'

if modulepath not in sys.path:
    sys.path.append(modulepath)


import setupcache
reload(setupcache)


if kwargs['altclick'] and kwargs['ctrlclick']:
    import uuid
    import setupcache_test
    reload(setupcache_test)

    print('\n')
    print('/'*50)
    print('/'*50)

    print('\n--> running cache setup tests...')
    print '--> test id: ', uuid.uuid1()
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


def get_sop_from_selection():
    selection = hou.selectedNodes()

    if selection:
        soptocache = selection[0]

        return soptocache
    else:
        print('>>> No Selection...')

        raise Exception('>>> No Selection...')


def create_nodes(localcache, soptocache):
    nodes = {'root': hou.node('/obj')}
    nodes['null'] = soptocache.createOutputNode('output', 'TO_CACHE_' + soptocache.name())
    nodes['read'] = nodes['null'].createOutputNode('file', 'READ_' + soptocache.name())

    if localcache:
        nodes['root'] = soptocache.parent()

    return nodes


def set_parms(nodes):
    nodes['read'].setDisplayFlag(True)
    nodes['read'].setRenderFlag(True)


def setup_cache(localcache):
    soptocache = get_sop_from_selection()
    nodes = create_nodes(localcache=localcache, soptocache=soptocache)

    set_parms(nodes)

    parmtemplate = hou.StringParmTemplate('rop', 'rop', 1,
                    string_type = hou.stringParmType.NodeReference)

    nodes['read'].addSpareParmTuple(parmtemplate)
    nodes['read'].parm("filemode").lock(True)
    nodes['read'].parm('file').set('`chs(chs("rop") + "/sopoutput")`')
    nodes['read'].setCurrent(True, clear_all_selected = True)

    if nodes['root'].node('cache'):
        nodes['ropnet'] = nodes['root'].node('cache')
    else:
        nodes['ropnet'] = nodes['root'].createNode('ropnet', 'Cache_Ropnet')

    nodes['ropnet'].moveToGoodPosition()

    nodes['rop'] = nodes['ropnet'].createNode('geometry', soptocache.name())
    nodes['read'].parm('rop').set(nodes['rop'].path())

    ropparms = {'soppath': nodes['null'].path(),
                'sopoutput': '{0}/$OS/$OS.$F4.bgeo.sc'.format('$CACHE'),
                'trange': 2,
                'mkpath': True,
                'saveretry': 2,
                }

    ropparmexpressions = {'f1': '$FSTART', 'f2': '$FEND + 1'}

    if localcache:
        ropparms['soppath'] = nodes['rop'].relativePathTo(nodes['null'])
        nodes['read'].parm('rop').set(nodes['read'].relativePathTo(nodes['rop']))

    nodes['rop'].setParms(ropparms)
    nodes['rop'].setParmExpressions(ropparmexpressions)

    return nodes


def main(kwargs):
    localcache = kwargs.get('ctrlclick', None)

    setup_cache(localcache)


if __name__ == '__main__':
    pass
