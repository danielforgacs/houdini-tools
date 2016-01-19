"""
tests for cache setup module
"""

import unittest
import random
import hou
import setupcache
reload(setupcache)



class HipTest(unittest.TestCase):
    """
    base class to initiate empty houdini scene
    across tests with a basic node network
    """

    def setUp(self):
        hou.hipFile.clear(suppress_save_prompt=True)

        geo = hou.node('/obj').createNode('geo', 'TEST_geo')
        geo.node('file1').destroy()

        name = ''. join([random.choice('qwertyuiop') for k in range(10)])
        box = geo.createNode('box', name)
        box.createOutputNode('smooth')
        box.createOutputNode('smooth')
        box.setSelected(True)
        box.setCurrent(True)


class SetupCacheTests(HipTest):
    """
    cache setup untit tests
    """

    def setUp(self):
        super(SetupCacheTests, self).setUp()

    def test_unittests_running(self):
        self.assertTrue(True)

    def test__get_sop_from_selection__returns_node(self):
        self.assertTrue(setupcache.get_sop_from_selection())

    def test__get_sop_from_selection__returns_sop(self):
        node = setupcache.get_sop_from_selection()

        self.assertIsInstance(node, hou.SopNode)

    def test__get_sop_from_selection__no_selection_gives_error(self):
        selection = hou.selectedNodes()[0]
        selection.setCurrent(False)

        self.assertRaises(setupcache.get_sop_from_selection)

    def test__create_nodes__returns_node_dict(self):
        selection = hou.selectedNodes()[0]
        nodeslocal = setupcache.create_nodes(localcache=True, soptocache=selection)
        nodesglobal = setupcache.create_nodes(localcache=False, soptocache=selection)

        self.assertIsInstance(nodeslocal, dict)
        self.assertIsInstance(nodesglobal, dict)

    def test__create_nodes__returns_number_of_nodes(self):
        selection = hou.selectedNodes()[0]
        nodeslocal = setupcache.create_nodes(localcache=True, soptocache=selection)
        nodesglobal = setupcache.create_nodes(localcache=False, soptocache=selection)

        self.assertEqual(len(nodeslocal), 1)
        self.assertEqual(len(nodesglobal), 1)

    def test__create_nodes__returns_houdini_nodes(self):
        selection = hou.selectedNodes()[0]
        nodeslocal = setupcache.create_nodes(localcache=True, soptocache=selection)
        nodesglobal = setupcache.create_nodes(localcache=False, soptocache=selection)

        for node in nodeslocal:
            self.assertIsInstance(nodeslocal[node], hou.Node)
            self.assertIsInstance(nodesglobal[node], hou.Node)

    def test__create_nodes__nodes_type_match(self):
        selection = hou.selectedNodes()[0]
        nodeslocal = setupcache.create_nodes(localcache=True, soptocache=selection)
        nodesglobal = setupcache.create_nodes(localcache=False, soptocache=selection)

        localtypes = {'root': 'geo'}

        for node in nodeslocal:
            self.assertEqual(nodeslocal[node].type().name(), localtypes[node])

    def test__create_nodes__global_local_nodes_match_except_root(self):
        selection = hou.selectedNodes()[0]
        nodeslocal = setupcache.create_nodes(localcache=True, soptocache=selection)
        nodesglobal = setupcache.create_nodes(localcache=False, soptocache=selection)

        nodeslocal.pop('root')
        nodesglobal.pop('root')

        self.assertEqual(nodeslocal, nodesglobal)

    def test__create_nodes__roots_are_proper_nodes(self):
        selection = hou.selectedNodes()[0]
        nodeslocal = setupcache.create_nodes(localcache=True, soptocache=selection)
        nodesglobal = setupcache.create_nodes(localcache=False, soptocache=selection)

        self.assertEqual(nodeslocal['root'], selection.parent())
        self.assertEqual(nodesglobal['root'], hou.node('/obj'))


class SetupCacheFunctonalTests(HipTest):
    """
    cache setup functional tests
    """

    def setUp(self):
        super(SetupCacheFunctonalTests, self).setUp()
        self.soptocache = hou.selectedNodes()[0]

    def functional_test(self, local=True):
        """
        unform test for local & global cache setups.
        called from separate tests with argument
        """
        ### module creates output
        soptocacheoutputs = self.soptocache.outputs()
        outtocache = soptocacheoutputs[len(soptocacheoutputs) - 1]

        self.assertGreaterEqual(len(soptocacheoutputs), 0)

        ### last output is sopnode output type
        self.assertIn(hou.SopNode, [type(k) for k in soptocacheoutputs])
        self.assertTrue(outtocache.type().name() == 'output')

        ### output name starts with TO_CACHE
        self.assertTrue('TO_CACHE' in outtocache.name())

        ### output's name contains sop to cache's name
        self.assertTrue(self.soptocache.name() in outtocache.name())

        ### output has one file output
        cacheread = outtocache.outputs()[0]

        self.assertTrue(cacheread.type().name() == 'file')

        ## cache file's name is 'READ_' + selected node's name
        self.assertTrue(self.soptocache.name() in cacheread.name())
        self.assertTrue(cacheread.name() == 'READ_' + self.soptocache.name())

        ### cache file is the current selection
        selection = hou.selectedNodes()[0]

        self.assertTrue(selection == cacheread)
        self.assertEqual(selection, cacheread)

        ### module creates local rop network if it doesn't exists
        geo = cacheread.parent()

        if local:
            ropnet = geo.node('Cache_Ropnet')
        else:
            ropnet = hou.node('/obj/Cache_Ropnet')

        self.assertTrue(geo.path() == self.soptocache.parent().path())
        self.assertTrue(ropnet)

        ### modeule creates sop rop node inside ropnet
        ### with the name of the node to cache
        self.assertTrue(ropnet.node(self.soptocache.name()))

        rop = ropnet.node(self.soptocache.name())

        ### cache sop node is linked to output
        if local:
            self.assertEqual(rop.parm('soppath').eval(), rop.relativePathTo(outtocache))
        else:
            self.assertEqual(rop.parm('soppath').eval(), outtocache.path())

        ### file output is set to cache folder
        ### and file name contains cached node's name
        filenamevalue = rop.parm('sopoutput').eval()
        filename = rop.parm('sopoutput').unexpandedString()

        self.assertEqual(filename, '$CACHE/$OS/$OS.$F4.bgeo.sc')
        self.assertIn(self.soptocache.name(), filenamevalue)

        ### cache frame range is global render frame range + 1
        ### frame range is expression
        startframe, endframe, stepping = rop.parmTuple('f').eval()

        self.assertEqual(startframe, int(hou.expandString('$FSTART')))
        self.assertEqual(endframe, int(hou.expandString('$FEND')) + 1)
        self.assertEqual(rop.parm('f1').expression(), '$FSTART')
        self.assertEqual(rop.parm('f2').expression(), '$FEND + 1')

        ### file cache node has spare parameter
        ### linking to the cache rop node
        self.assertTrue(cacheread.parm('rop'))

        if local:
            self.assertEqual(cacheread.relativePathTo(rop), cacheread.parm('rop').eval())
        else:
            self.assertEqual(rop.path(), cacheread.parm('rop').eval())

        ### test for various rop node parms
        self.assertEqual(rop.parm('trange').eval(), 2)
        self.assertTrue(rop.parm('mkpath').eval())
        self.assertEqual(rop.parm('saveretry').eval(), 2)
        self.assertTrue(rop.parm('savebackground').eval())

    def test_01_local_cache(self):
        local = True
        setupcache.main({'ctrlclick': local})

        self.functional_test(local=local)

    def test_02_global_cache(self):
        local = False
        setupcache.main({'ctrlclick': local})

        self.functional_test(local=local)



def main():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(SetupCacheTests)
    suite_func = loader.loadTestsFromTestCase(SetupCacheFunctonalTests)

    unittest.TextTestRunner(verbosity=1).run(suite)
    unittest.TextTestRunner(verbosity=1).run(suite_func)


if __name__ == '__main__':
    main()
