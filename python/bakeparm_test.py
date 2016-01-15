"""
"""


import unittest
import hou
import bakeparm



class BakeParmTests(unittest.TestCase):
    def setUp(self):
        self.geo = hou.node('/obj').createNode('geo', 'TEST_geo')

    def tearDown(self):
        self.geo.destroy()

    def test_get_frame_range_returns_tuple(self):
        self.assertTrue(type(bakeparm.get_frame_range()) is tuple)


def main():
    print('\n'*5)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(BakeParmTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
