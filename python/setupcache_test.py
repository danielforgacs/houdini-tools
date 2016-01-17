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


# class SetupCacheNewTests(HipTest):
#     """
#     unit tests new
#     """

#     def test__get_sop_from_selection__returns_sop(self):
#         node = setupcache.get_sop_from_selection()

#         self.assertTrue(type(node) is hou.SopNode)
#         self.assertTrue(type(node.type()) is hou.SopNodeType)
#         self.assertTrue(isinstance(node.type(), hou.SopNodeType))
#         self.assertIsInstance(node.type(), hou.SopNodeType)


class SetupCacheTests(HipTest):
    """
    cache setup untit tests
    """

    def setUp(self):
        pass

    def test_unittests_running(self):
        self.assertTrue(True)


class SetupCacheFunctonalTests(HipTest):
    """
    cache setup functional tests
    """

    def setUp(self):
        super(SetupCacheFunctonalTests, self).setUp()
        self.soptocache = hou.selectedNodes()[0]
        setupcache.main({'ctrlclick': True})

    def test_functest_local_cache(self):
        ### module creates output
        outputs = self.soptocache.outputs()
        self.assertGreaterEqual(len(outputs), 0)
        cacheout = outputs[len(outputs) - 1]

        ### last output is sopnode output type
        self.assertIn(hou.SopNode, [type(k) for k in outputs])
        self.assertTrue(cacheout.type().name() == 'output')

        ### output name starts with TO_CACHE
        self.assertTrue('TO_CACHE' in cacheout.name())

        ### output's name contains node
        self.assertTrue(self.soptocache.name() in cacheout.name())

        ### output has one file output
        cachefile = cacheout.outputs()[0]

        self.assertTrue(cachefile.type().name() == 'file')

        ## cache file's name is 'READ_' + selected node's name
        self.assertTrue(self.soptocache.name() in cachefile.name())
        self.assertTrue(cachefile.name() == 'READ_' + self.soptocache.name())

        ### cache file is the current selection
        cachefile = hou.selectedNodes()[0]
        self.assertTrue(cachefile.type().name() == 'file')

        ### module creates rop network if it doesn't exists
        geo = cachefile.parent()

        self.assertTrue(geo.path() == self.soptocache.parent().path())
        self.assertTrue(geo.node('Cache_Ropnet'))

        ### modeule creates sop rop node inside ropnet
        ### with the name of the node to cache
        ropnet = geo.node('Cache_Ropnet')

        self.assertTrue(ropnet.node(self.soptocache.name()))

        ### cache sop node is linked to output

        ### file output is set to cache folder
        ### and file name contains cached node's name

        ### file cache node has spare parameter
        ### linking to the cache rop node



def main():
    print('\n.'*8)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(SetupCacheTests)
    suite_func = loader.loadTestsFromTestCase(SetupCacheFunctonalTests)

    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.TextTestRunner(verbosity=2).run(suite_func)


if __name__ == '__main__':
    main()
