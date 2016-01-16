import unittest
import hou
import setupcache
reload(setupcache)



class SetupCacheTests(unittest.TestCase):
    def setUp(self):
        hou.hipFile.clear(suppress_save_prompt=True)

        geo = hou.node('/obj').createNode('geo', 'TEST_geo')
        box = geo.createNode('box', 'box')
        self.out = box.createOutputNode('null', 'OUT_box_geo')

        geo.node('file1').destroy()
        self.out.setSelected(True)
        self.out.setCurrent(True)

    def tearDown(self):
        pass

    def test__get_sop_from_selection__returns_sop(self):
        node = setupcache.get_sop_from_selection()

        self.assertTrue(type(node) is hou.SopNode)
        self.assertTrue(type(node.type()) is hou.SopNodeType)
        self.assertTrue(isinstance(node.type(), hou.SopNodeType))


class SetupCacheFunctonalTests(unittest.TestCase):
    def setUp(self):
        hou.hipFile.clear(suppress_save_prompt=True)

        geo = hou.node('/obj').createNode('geo', 'TEST_geo')
        box = geo.createNode('box', 'box')
        self.out = box.createOutputNode('null', 'OUT_box_geo')

        geo.node('file1').destroy()
        self.out.setSelected(True)
        self.out.setCurrent(True)

    def test_setup_cache(self):
        setupcache.main2()

        outputs = self.out.outputConnections()
        self.assertGreaterEqual(len(outputs), 0)


def main():
    print('\n.'*8)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(SetupCacheTests)
    suite_func = loader.loadTestsFromTestCase(SetupCacheFunctonalTests)

    # unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.TextTestRunner(verbosity=2).run(suite_func)


if __name__ == '__main__':
    main()
